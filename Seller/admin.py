from django.contrib import admin
from django.contrib import messages
from Seller import models
import requests

def send_email(request, email_value, status, order):
    url = 'https://mail.dwine.me/api/v1/send-mail'

    # Generate HTML for order items
    order_items_html = ''

    order_items_html += f"""
        <tr>
            <td style="padding: 10px; text-align: left; display:grid; grid-template-columns: 3fr; width:100%;">
                <p style="margin: 0; font-weight: bold;">{order.product.name}</p>
                <p style="margin: 5px 0;">Order ID: {order.order_id}</p>
                <p style="margin: 0;">Price: ${order.price}</p>
            </td>
        </tr>
        """
    
    payload = {
        "authUser": "your_email",
        "authPass": "your_app_password",
        "To": email_value,
        "FromName": "ArtGround",
        "ReplyAddress": "your_email",
        "Subject": f"Your Order has been {status}",
        "Body": f"""
        <table
            style="width: 100%; max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; border-spacing: 0; background-color: #f9f9f9; border: 1px solid #e9e9e9; padding: 10px; border-radius: 15px;">
            <tr>
                <td style="padding: 20px; text-align: center; background-color: #4a68a9; border-radius: 10px 10px 0px 0px;">
                    <h1 style="color: #ffffff; margin: 0;">ArtGround</h1>
                    <p style="color: #ffffff; margin-top: 10px;">Your Order Status: {status}</p>
                </td>
            </tr>
            <tr>
                <td style="padding: 30px; background-color: #ffffff;">
                    <p style="font-size: 16px; color: #333333; line-height: 1.5; margin: 0 0 20px;">
                        Hi there,
                    </p>
                    <p style="font-size: 16px; color: #333333; line-height: 1.5; margin: 0 0 20px;">
                        We wanted to let you know that the status of your order has been updated to: 
                        <strong style="color: #4a68a9;">{status}</strong>.
                    </p>

                    <p style="font-size: 16px; color: #333333; line-height: 1.5; margin: 0 0 20px;">
                        Here are the details of your order:
                    </p>
                    <table style="width: 100%; margin-top: 20px; border-spacing: 0;">
                        {order_items_html}
                    </table>

                    <p style="font-size: 16px; color: #333333; line-height: 1.5; margin: 0 0 20px;">
                        If you have any questions or need further assistance, feel free to contact us.
                    </p>
                    <p style="font-size: 16px; color: #333333; line-height: 1.5; margin: 0;">
                        Thanks for choosing ArtGround!<br />
                        The ArtGround Team
                    </p>
                </td>
            </tr>
            <tr>
                <td style="padding: 15px; text-align: center; background-color: #4a68a9; border-radius: 0px 0px 10px 10px;">
                    <p style="color: #ffffff; font-size: 12px; margin: 0;">
                        © 2024 ArtGround | All rights reserved
                    </p>
                </td>
            </tr>
        </table>
        """,
        }

    headers = {
            'Content-Type': 'application/json',
        }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            messages.success(request, "Email sent successfully.")
        else:
            messages.error(request, f"Failed to send email. Status Code: {response.status_code}")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

@admin.action(description='Mark Selected Orders as Rejected')
def order_rejected(modeladmin, request, queryset):
    queryset.update(status=models.OrderItem.Status_choices.REJECTED)
    for order in queryset:
        send_email(request, order.order.user.email, 'Rejected', order)

@admin.action(description='Mark Selected Orders as Accepted')
def order_accepted(modeladmin, request, queryset):
    queryset.update(status=models.OrderItem.Status_choices.ACCEPTED)
    for order in queryset:
        send_email(request, order.order.user.email, 'Accepted', order)

@admin.action(description='Mark Selected Orders as Packed')
def order_packed(modeladmin, request, queryset):
    queryset.update(status=models.OrderItem.Status_choices.PACKED)
    for order in queryset:
        send_email(request, order.order.user.email, 'Packed', order)

@admin.action(description='Mark Selected Orders as Shipped')
def order_shipped(modeladmin, request, queryset):
    queryset.update(status=models.OrderItem.Status_choices.SHIPPED)
    for order in queryset:
        send_email(request, order.order.user.email, 'Shipped', order)

@admin.action(description='Mark Selected Orders as Delivered')
def order_delivered(modeladmin, request, queryset):
    queryset.update(status=models.OrderItem.Status_choices.DELIVERED)
    for order in queryset:
        send_email(request, order.order.user.email, 'Delivered', order)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_item_id', 'order', 'product', 'quantity', 'price', 'status']
    actions = [order_rejected, order_accepted, order_packed, order_shipped, order_delivered]

# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderItem, OrderItemAdmin)
