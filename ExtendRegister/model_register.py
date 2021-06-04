# -*- coding: utf-8 -*-
# @Time    : 2021/5/31 上午10:37
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : model_register.py
# @Software: PyCharm

from app.models.admin.models import Admin, Role, Permission, MidAdminAndRole, MidPermissionAndRole, ApiResource, \
    RouteResource
from app.models.product.models import ProductBrand, ProductCategory, Product, Sku, AttributeKey, AttributeVal, \
    ProductComment, ProductStock, ProductSales, ProductOperationLog
from app.models.order.models import Order, OrderItem, OrderSnapshot
