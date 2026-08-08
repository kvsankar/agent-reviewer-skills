## Anti-Patterns - Common Mistakes

### ANTI-FAT-MODELS: Avoid Fat Models

**Principle:** Keep models focused on data and simple business logic. Use services for complex operations.

**Bad Example:**
```python
# Fat model with too much responsibility
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    def process_payment(self, payment_method):
        # Payment processing logic
        if payment_method == 'credit_card':
            response = stripe.Charge.create(amount=self.total, ...)
        elif payment_method == 'paypal':
            response = paypal.charge(self.total, ...)
        # ... 50 more lines

    def send_confirmation_email(self):
        # Email logic
        # ... 30 lines

    def update_inventory(self):
        # Inventory logic
        # ... 40 lines

    def generate_invoice_pdf(self):
        # PDF generation
        # ... 60 lines

    # Model has 200+ lines of business logic!
```

**Good Example:**
```python
# Thin model - just data and simple methods
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'

    def is_paid(self):
        return self.status == 'paid'

# Service layer for business logic
# services/order_service.py
class OrderService:
    @staticmethod
    def process_payment(order, payment_method, payment_details):
        """Process payment for an order"""
        payment_service = PaymentService()

        try:
            charge = payment_service.charge(
                amount=order.total,
                method=payment_method,
                details=payment_details
            )

            order.status = 'paid'
            order.save()

            return charge
        except PaymentError as e:
            logger.error(f'Payment failed for order {order.id}: {e}')
            raise

    @staticmethod
    def complete_order(order):
        """Complete order processing workflow"""
        # Update inventory
        InventoryService.reserve_items(order.items.all())

        # Send email
        EmailService.send_order_confirmation(order)

        # Generate invoice
        InvoiceService.generate_pdf(order)

        # Update status
        order.status = 'completed'
        order.save()

# services/payment_service.py
class PaymentService:
    def charge(self, amount, method, details):
        if method == 'credit_card':
            return self._charge_credit_card(amount, details)
        elif method == 'paypal':
            return self._charge_paypal(amount, details)
        else:
            raise ValueError(f'Unknown payment method: {method}')

    def _charge_credit_card(self, amount, details):
        # Stripe integration
        return stripe.Charge.create(
            amount=int(amount * 100),
            currency='usd',
            source=details['token'],
        )

    def _charge_paypal(self, amount, details):
        # PayPal integration
        pass

# Using services in views
from myapp.services.order_service import OrderService

def checkout(request):
    order = get_object_or_404(Order, id=request.POST['order_id'])

    try:
        OrderService.process_payment(
            order=order,
            payment_method=request.POST['payment_method'],
            payment_details=request.POST.get('payment_details')
        )

        OrderService.complete_order(order)

        return JsonResponse({'status': 'success'})
    except PaymentError as e:
        return JsonResponse({'error': str(e)}, status=400)
```

**Why this matters:**
Fat models cause:
- Tight coupling
- Hard to test
- Hard to maintain
- Violates single responsibility principle

**Best practice:**
Keep models thin - just data and simple methods. Use service layer for business logic. Use managers/querysets for data access logic. Separate concerns.

---

