## API Design - Django REST Framework

### API-SERIAL: Serializer Best Practices

**Principle:** Design serializers that are secure, efficient, and maintainable.

**Bad Example:**
```python
# Exposing sensitive fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # DANGEROUS: Exposes password hash, email, etc.

# No validation
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']
    # No validation of content length, format, etc.

# N+1 queries in serializer
class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username')  # N+1!
    category_name = serializers.CharField(source='category.name')  # N+1!

    class Meta:
        model = Post
        fields = ['title', 'author_name', 'category_name']
```

**Good Example:**
```python
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# Explicit fields, no sensitive data
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

# Different serializers for different contexts
class UserListSerializer(serializers.ModelSerializer):
    """Minimal data for list view"""
    class Meta:
        model = User
        fields = ['id', 'username']

class UserDetailSerializer(serializers.ModelSerializer):
    """More data for detail view"""
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',
                  'date_joined', 'post_count']

class UserCreateSerializer(serializers.ModelSerializer):
    """For user registration"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

# Nested serializers with select_related/prefetch_related
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PostSerializer(serializers.ModelSerializer):
    # Use nested serializers, but optimize queryset in view
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tag_names = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'category',
                  'tag_names', 'created_at']

    def get_tag_names(self, obj):
        # Assumes tags are prefetched in view
        return [tag.name for tag in obj.tags.all()]

# View with optimized queryset
class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.select_related(
            'author', 'category'
        ).prefetch_related('tags').all()

# Validation in serializers
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Title must be at least 10 characters long"
            )

        # Check uniqueness
        if Post.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError(
                "A post with this title already exists"
            )

        return value

    def validate_content(self, value):
        if len(value) < 100:
            raise serializers.ValidationError(
                "Content must be at least 100 characters long"
            )

        # Check for spam
        if contains_spam(value):
            raise serializers.ValidationError(
                "Content contains inappropriate content"
            )

        return value

    def validate(self, data):
        # Cross-field validation
        if data['title'].lower() in data['content'].lower():
            raise serializers.ValidationError(
                "Title should not be repeated in content"
            )

        return data

# Writable nested serializers
class PostWithTagsSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True
    )
    tag_list = CategorySerializer(source='tags', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'tags', 'tag_list']

    def create(self, validated_data):
        tag_names = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)

        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return post
```

**Why this matters:**
Poor serializers cause:
- Security issues (exposed sensitive data)
- N+1 query problems
- Invalid data in database
- Poor API usability

**Best practice:**
Explicitly define fields. Use different serializers for different contexts (list, detail, create, update). Validate data. Optimize with select_related/prefetch_related in views.

---

### API-PERM: API Permissions and Authentication

**Principle:** Implement proper authentication and permission checks for all API endpoints.

**Bad Example:**
```python
# No authentication required
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Anyone can read, create, update, delete any post!

# Authentication but no authorization
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Authenticated users can delete any post!
```

**Good Example:**
```python
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Custom permission
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their posts.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for author
        return obj.author == request.user

# ViewSet with proper permissions
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        # Users only see their own posts for edit/delete
        if self.action in ['update', 'partial_update', 'destroy']:
            return Post.objects.filter(author=self.request.user)
        return Post.objects.all()

    def perform_create(self, serializer):
        # Set author to current user
        serializer.save(author=self.request.user)

# Token authentication
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT authentication (more secure for SPAs)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Different permissions for different actions
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [permissions.AllowAny]
        else:  # update, destroy
            permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

        return [permission() for permission in permission_classes]

# Custom action with permission
class PostViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        post = self.get_object()

        # Check if user can publish
        if post.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to publish this post.'},
                status=status.HTTP_403_FORBIDDEN
            )

        post.status = 'published'
        post.published_at = timezone.now()
        post.save()

        return Response({'status': 'Post published'})

# Object-level permissions with django-guardian
from guardian.shortcuts import assign_perm, get_objects_for_user

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show documents user has permission to view
        return get_objects_for_user(
            self.request.user,
            'documents.view_document'
        )

    def perform_create(self, serializer):
        document = serializer.save(owner=self.request.user)
        # Assign permissions to creator
        assign_perm('view_document', self.request.user, document)
        assign_perm('change_document', self.request.user, document)
        assign_perm('delete_document', self.request.user, document)
```

**Why this matters:**
Without proper API security:
- Unauthorized data access
- Data modification/deletion by wrong users
- API abuse
- Regulatory compliance violations

**Best practice:**
Always require authentication by default. Use object-level permissions. Use JWT for SPAs. Implement different permissions for different actions. Rate limit APIs.

---

### API-THROTTLE: Rate Limiting

**Principle:** Implement rate limiting to prevent abuse and ensure fair usage.

**Bad Example:**
```python
# No rate limiting
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [],
    # API can be hammered with unlimited requests
}
```

**Good Example:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # 100 requests per hour for anonymous users
        'user': '1000/hour',  # 1000 requests per hour for authenticated users
    }
}

# Custom throttle for specific endpoints
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'myapp.throttles.BurstRateThrottle',
        'myapp.throttles.SustainedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',      # Max 60 requests per minute
        'sustained': '1000/day', # Max 1000 requests per day
    }
}

# Per-view throttling
class PostViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'posts'

    # settings.py: 'posts': '100/hour'

# Different throttle for different actions
class PostViewSet(viewsets.ModelViewSet):
    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [BurstRateThrottle]  # Stricter for creates
        else:
            throttle_classes = [SustainedRateThrottle]

        return [throttle() for throttle in throttle_classes]

# Custom throttle based on user tier
from rest_framework.throttling import SimpleRateThrottle

class PremiumUserRateThrottle(SimpleRateThrottle):
    scope = 'premium'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

    def allow_request(self, request, view):
        # Premium users get higher rate limit
        if request.user.is_authenticated and request.user.is_premium:
            self.rate = '10000/hour'
        else:
            self.rate = '1000/hour'

        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)
```

**Why this matters:**
Without rate limiting:
- API abuse and DoS attacks
- Resource exhaustion
- Unfair usage
- High infrastructure costs

**Best practice:**
Always implement rate limiting. Use different rates for anon vs authenticated. Use stricter limits for expensive operations. Consider user tiers for different limits.

---

