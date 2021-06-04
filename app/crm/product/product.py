# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 下午5:58
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : product.py
# @Software: PyCharm


from app.all_reference import *
from app.models.product.models import Product, Sku, ProductStock


# Todo 商品编辑
# Todo 操作日志
class ProductCrmApi(Resource):
    """
    商品
    GET: 商品详情
    POST: 商品新增
    PUT: 商品编辑
    DELETE: 商品逻辑删除
    """

    def get(self, product_id=None):
        prod_obj = Product.query.get(product_id)
        if prod_obj:
            prod = prod_obj.to_json()
            sku_list = Sku.query.filter_by(product_id=product_id).all()
            if sku_list:
                prod['sku_list'] = [s.to_json() for s in sku_list]
            else:
                prod['sku_list'] = []
            return api_result(code=200, message='操作成功', data=prod)
        else:
            ab_code_2(1000001)

    def post(self):
        data = request.get_json()
        prod_category = data.get('prod_category')
        name = data.get('name')
        summary = data.get('summary')
        price = data.get('price')
        cost_price = data.get('cost_price')
        sale_price = data.get('sale_price')
        sale_status = data.get('sale_status')
        cover_picture = data.get('cover_picture')
        video = data.get('video')
        carousel = data.get('carousel')
        image_link_dict = data.get('image_link_dict')
        remark = data.get('remark')
        prod_stock = data.get('stock')
        sku_list = data.get('sku_list')

        new_prod = Product(
            prod_category_id=prod_category,
            name=name,
            summary=summary,
            price=price,
            cost_price=cost_price,
            sale_price=sale_price,
            sale_status=sale_status,
            prod_status=3,
            cover_picture=cover_picture,
            video=video,
            carousel=carousel,
            image_link_dict=image_link_dict,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        db.session.add(new_prod)
        db.session.commit()

        product_id = new_prod.id

        if sku_list:
            for sku in sku_list:
                icon = sku.get('icon')
                spec = sku.get('spec')
                price = sku.get('price')
                cost_price = sku.get('cost_price')
                sale_price = sku.get('sale_price')
                sku_stock = sku.get('stock')
                remark = sku.get('remark')
                new_sku = Sku(
                    product_id=product_id,
                    icon=icon,
                    spec=spec,
                    price=price,
                    cost_price=cost_price,
                    sale_price=sale_price,
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark=remark
                )
                db.session.add(new_sku)
                db.session.commit()
                ps = ProductStock(sku_id=new_sku.id, stock=sku_stock)
                db.session.add(ps)
            db.session.commit()
        else:
            ps = ProductStock(product_id=product_id, stock=prod_stock)
            db.session.add(ps)
            db.session.commit()
        return api_result(code=201, message='操作成功', data=data)

    def put(self):
        data = request.get_json()
        return api_result(code=203, message='操作成功', data=[])

    def delete(self):
        data = request.get_json()
        product_id = int(data.get('product_id'))
        prod_status = int(data.get('prod_status'))
        prod = Product.query.get(product_id)
        if prod and prod_status in [1, 2, 3, 4, 5]:
            prod.prod_status = prod_status
            prod.modifier = g.app_user.username
            prod.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=204, message='操作成功', data=[])
        else:
            ab_code_2(1000001)
