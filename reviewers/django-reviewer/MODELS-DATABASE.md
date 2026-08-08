## Models & Database - Performance and Integrity

### MODEL-N+1: Avoid N+1 Query Problems

**Principle:** Use `select_related()` and `prefetch_related()` to avoid N+1 query issues.

**Bad Example:**
```python
# N+1 query problem
def get_posts_with_authors(request):
    posts = Post.objects.all()  # 1 query

    # This creates N additional queries (one per post)
    for post in posts:
        print(post.author.name)  # N queries!

    return render(request, 'posts.html', {'posts': posts})

# In template this also causes N+1:
# {% for post in posts %}
#   {{ post.author.name }}  <!-- Query per post -->
# {% endfor %}
```

**Good Example:**
```python
# Using select_related for ForeignKey/OneToOne
def get_posts_with_authors(request):
    # select_related() does a SQL JOIN
    posts = Post.objects.select_related('author').all()  # 1 query total

    # No additional queries
    for post in posts:
        print(post.author.name)

    return render(request, 'posts.html', {'posts': posts})

# Using prefetch_related for ManyToMany/reverse ForeignKey
def get_posts_with_tags(request):
    # prefetch_related() does separate queries and joins in Python
    posts = Post.objects.prefetch_related('tags').all()  # 2 queries total

    for post in posts:
        print([tag.name for tag in post.tags.all()])  # No additional queries

    return render(request, 'posts.html', {'posts': posts})

# Combining both:
def get_complete_posts(request):
    posts = (
        Post.objects
        .select_related('author', 'category')  # ForeignKeys
        .prefetch_related('tags', 'comments')  # ManyToMany and reverse FK
        .all()
    )
    return render(request, 'posts.html', {'posts': posts})

# Custom prefetch for filtered related objects:
from django.db.models import Prefetch

def get_posts_with_recent_comments(request):
    recent_comments = Comment.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    )

    posts = Post.objects.prefetch_related(
        Prefetch('comments', queryset=recent_comments, to_attr='recent_comments')
    ).all()

    return render(request, 'posts.html', {'posts': posts})
```

**Why this matters:**
N+1 queries are the #1 Django performance issue:
- 100 posts = 101 queries instead of 1-2
- Massive database load at scale
- Slow page loads and timeouts
- Database connection exhaustion

**Best practice:**
Use Django Debug Toolbar to detect N+1 queries. Always use `select_related()` for ForeignKey/OneToOne, `prefetch_related()` for ManyToMany/reverse ForeignKey.

---

### MODEL-INDEX: Database Indexing

**Principle:** Add database indexes on fields used in queries, especially for filtering, ordering, and foreign keys.

**Bad Example:**
```python
# models.py
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # No index
    created_at = models.DateTimeField(auto_now_add=True)  # No index
    total = models.DecimalField(max_digits=10, decimal_places=2)  # No index

# views.py
def get_pending_orders(request):
    # Slow query without indexes
    orders = Order.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})
```

**Good Example:**
```python
# models.py
class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True  # Automatically indexed by Django
    )
    status = models.CharField(
        max_length=20,
        db_index=True  # Index for filtering
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True  # Index for ordering
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # Composite index for common query pattern
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['-created_at']),  # For ordering by latest
        ]
        # Ordering automatically creates index
        ordering = ['-created_at']

# For unique constraints (which create indexes):
class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)  # Automatically indexed
    slug = models.SlugField(unique=True)  # Automatically indexed

    class Meta:
        # Composite unique constraint
        unique_together = [['category', 'slug']]

# Partial indexes (PostgreSQL):
from django.db.models import Index, Q

class Article(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)

    class Meta:
        indexes = [
            # Index only published articles
            Index(
                fields=['title'],
                name='published_title_idx',
                condition=Q(status='published')
            ),
        ]
```

**Why this matters:**
Missing indexes cause:
- Full table scans on large tables
- Slow queries (seconds/minutes instead of milliseconds)
- Database CPU/IO overload
- Timeouts and poor user experience

**Best practice:**
Index fields used in `filter()`, `exclude()`, `order_by()`. Use composite indexes for multi-field queries. Monitor slow queries with database logs. Don't over-index (updates become slower).

---

### MODEL-QUERY: Query Optimization

**Principle:** Write efficient queries using Django ORM features. Avoid loading unnecessary data.

**Bad Example:**
```python
# Loading all fields when only need a few
def get_user_names():
    users = User.objects.all()  # Loads all fields
    return [user.username for user in users]

# Loading all objects when you just need count
def count_active_users():
    users = User.objects.filter(is_active=True)
    return len(list(users))  # Loads all objects into memory!

# Inefficient existence check
def user_exists(email):
    users = User.objects.filter(email=email)
    return len(users) > 0  # Loads objects just to check existence

# Loading full objects for deletion
def delete_old_logs():
    old_logs = Log.objects.filter(created_at__lt=cutoff_date)
    for log in old_logs:
        log.delete()  # N delete queries!
```

**Good Example:**
```python
# Use only() / defer() to load specific fields
def get_user_names():
    # Only load username field
    users = User.objects.only('username')
    return [user.username for user in users]

# Use values() / values_list() for simple data
def get_user_names_efficient():
    # Returns list of usernames, doesn't create model instances
    return list(User.objects.values_list('username', flat=True))

# Use count() for counting
def count_active_users():
    return User.objects.filter(is_active=True).count()  # Database COUNT()

# Use exists() for existence checks
def user_exists(email):
    return User.objects.filter(email=email).exists()  # Efficient EXISTS query

# Bulk operations for updates/deletes
def delete_old_logs():
    cutoff_date = timezone.now() - timedelta(days=90)
    # Single DELETE query
    Log.objects.filter(created_at__lt=cutoff_date).delete()

def mark_orders_shipped(order_ids):
    # Single UPDATE query
    Order.objects.filter(id__in=order_ids).update(
        status='shipped',
        shipped_at=timezone.now()
    )

# Bulk create for multiple inserts
def create_tags(tag_names):
    tags = [Tag(name=name) for name in tag_names]
    # Single INSERT with multiple values
    Tag.objects.bulk_create(tags)

# Use iterator() for large querysets
def process_all_orders():
    # Prevents loading all objects into memory
    for order in Order.objects.iterator(chunk_size=1000):
        process_order(order)

# Aggregate queries
from django.db.models import Count, Avg, Sum

def get_order_stats():
    stats = Order.objects.aggregate(
        total_orders=Count('id'),
        average_total=Avg('total'),
        total_revenue=Sum('total')
    )
    return stats

# Annotate queries
def get_users_with_order_count():
    users = User.objects.annotate(
        order_count=Count('order')
    ).filter(order_count__gt=0)
    return users
```

**Why this matters:**
Inefficient queries cause:
- Excessive memory usage
- Slow response times
- High database load
- Unnecessary data transfer

**Best practice:**
Use `values()`, `values_list()` for simple data. Use `only()`, `defer()` for specific fields. Use `count()`, `exists()` for checks. Use bulk operations for multiple updates/deletes.

---

### MODEL-MIGRATION: Migration Management

**Principle:** Keep migrations clean, reversible, and production-safe.

**Bad Example:**
```python
# Migration with data loss
class Migration(migrations.Migration):
    operations = [
        migrations.RemoveField(
            model_name='order',
            name='old_status',  # Data lost immediately!
        ),
    ]

# Non-reversible migration
class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(
            code=forward_migration,
            # No reverse_code provided - not reversible!
        ),
    ]

# Migration that breaks in production
class Migration(migrations.Migration):
    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(max_digits=8, decimal_places=2),
            # If existing data has more than 8 digits, this fails!
        ),
    ]
```

**Good Example:**
```python
# Safe field removal - three-step process:
# Step 1: Make field nullable
class Migration(migrations.Migration):
    operations = [
        migrations.AlterField(
            model_name='order',
            name='old_status',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]

# Step 2: Deploy code that doesn't use the field, then remove from model

# Step 3: Remove field in separate migration after deployed
class Migration(migrations.Migration):
    operations = [
        migrations.RemoveField(
            model_name='order',
            name='old_status',
        ),
    ]

# Reversible data migration
def forward_migration(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Order.objects.filter(old_status='shipped').update(new_status='delivered')

def reverse_migration(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Order.objects.filter(new_status='delivered').update(old_status='shipped')

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(
            code=forward_migration,
            reverse_code=reverse_migration  # Reversible!
        ),
    ]

# Safe field changes with validation
class Migration(migrations.Migration):
    operations = [
        # First check data won't break:
        migrations.RunPython(
            code=validate_price_data,
            reverse_code=migrations.RunPython.noop
        ),
        # Then make change:
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]

# Safe adding of non-null fields:
# Step 1: Add nullable
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                'Category',
                on_delete=models.CASCADE,
                null=True,  # Initially nullable
                blank=True
            ),
        ),
    ]

# Step 2: Populate data
class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(
            code=populate_category,
            reverse_code=migrations.RunPython.noop
        ),
    ]

# Step 3: Make non-null
class Migration(migrations.Migration):
    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                'Category',
                on_delete=models.CASCADE,
            ),
        ),
    ]
```

**Why this matters:**
Bad migrations cause:
- Production downtime
- Data loss
- Failed deployments
- Difficult rollbacks

**Best practice:**
Test migrations on production-like data. Make changes in small, reversible steps. Use `--check` flag to test. Keep migrations squashed periodically. Never edit applied migrations.

---

### MODEL-CONSTRAINT: Database Constraints

**Principle:** Use database constraints to enforce data integrity at the database level.

**Bad Example:**
```python
# models.py
class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    # No constraint that discount <= total

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    # No constraint that quantity >= 0
    # No unique constraint on product

# Relying on application logic only:
def create_order(total, discount):
    if discount > total:
        raise ValueError("Discount cannot exceed total")
    return Order.objects.create(total=total, discount=discount)
```

**Good Example:**
```python
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(discount__lte=models.F('total')),
                name='discount_lte_total'
            ),
            CheckConstraint(
                check=Q(total__gte=0),
                name='total_non_negative'
            ),
        ]

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            # Quantity cannot be negative
            CheckConstraint(
                check=Q(quantity__gte=0),
                name='quantity_non_negative'
            ),
            # One inventory record per product per warehouse
            UniqueConstraint(
                fields=['product', 'warehouse'],
                name='unique_product_warehouse'
            ),
        ]

class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(end_date__gte=models.F('start_date')),
                name='end_date_after_start_date'
            ),
        ]

# Unique constraints with conditions (PostgreSQL):
class Article(models.Model):
    slug = models.SlugField()
    status = models.CharField(max_length=20)

    class Meta:
        constraints = [
            # Slug must be unique among published articles
            UniqueConstraint(
                fields=['slug'],
                condition=Q(status='published'),
                name='unique_published_slug'
            ),
        ]
```

**Why this matters:**
Without database constraints:
- Data integrity depends solely on application code
- Race conditions can create invalid data
- Direct database access bypasses validation
- Bugs can corrupt data

**Best practice:**
Use CheckConstraint for business rules. Use UniqueConstraint for uniqueness. Constraints are enforced at database level, protecting against all access paths.

---

