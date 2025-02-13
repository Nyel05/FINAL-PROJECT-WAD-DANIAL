from django.db import models

# Product Table
class ProductDetails(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=100, default="Clothes")
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# User Table
class UserDetails(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Should be hashed
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# Order Table
class OrderDetails(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"), 
            ("Shipped", "Shipped"), 
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled")
        ],
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


# Cart Table
class CartItems(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, default="M")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"


# Payment Table
class Payment(models.Model):
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=50,
        choices=[("Credit Card", "Credit Card"), ("PayPal", "PayPal"), ("Cash On Delivery", "Cash On Delivery")],
        default="Cash On Delivery"
    )
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Failed", "Failed")],
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.order.id}"


# Admin Table
class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Should be hashed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# Order Items Table
class OrderItems(models.Model):
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=10, default='M')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.product_name} ({self.quantity}x) - Order #{self.order.id}"

    def save(self, *args, **kwargs):
        if not self.product_name:
            self.product_name = self.product.name
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
