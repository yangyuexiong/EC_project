# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 下午1:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : sku.py
# @Software: PyCharm


from app.all_reference import *
from app.models.product.models import Product, AttributeKey, AttributeVal, Sku, ProductStock


class SkuApi(Resource):
    """
    sku
    """

    def get(self):

        # q = Sku.query.join(Product, Sku.product_id == Product.id).order_by(Sku.create_time.desc())
        from sqlalchemy import or_
        q = ""
        like_list = [Product.name.ilike(q if q else ''), Product.summary.ilike(q if q else '')]
        q = db.session.query(Sku, Product).join(Product, Sku.product_id == Product.id).filter(
            or_(*like_list))
        for i in q.all():
            print(i)
            print(type(i[0]), type(i[1]))
            print(i[0].to_json())
            print(i[1].to_json())
            print('\n')
            # print(i.to_json())
            # print(i.to_json())
        return api_result(code=200, message='操作成功', data=[])

    def post(self):
        data = request.get_json()
        attr_list = data.get('attr_list', [])
        if attr_list and isinstance(attr_list, list):
            for attr in attr_list:
                attr_val = attr.get('attr_val', [])
                if attr_val:
                    prod_category_id = attr.get('category_id')
                    product_id = attr.get('product_id')
                    name = attr.get('attr_key')
                    remark = attr.get('remark')
                    ak = AttributeKey(
                        prod_category_id=prod_category_id, product_id=product_id, name=name, remark=remark)
                    db.session.add(ak)
                    db.session.commit()
                    for av in attr_val:
                        new_av = AttributeVal(attr_key_id=ak.id, name=av)
                        db.session.add(new_av)
                    db.session.commit()
                else:
                    ab_code_2(1000001)
            return api_result(code=200, message='操作成功', data=data)
        else:
            ab_code_2(1000001)

    def put(self):
        data = request.get_json()
        attr_key_id = int(data.get('attr_key_id', 0))
        category_id = data.get('category_id')
        product_id = data.get('product_id')
        attr_key = data.get('attr_key')
        attr_val_list = data.get('attr_val_list', [])

        if attr_val_list and isinstance(attr_val_list, list):
            func = lambda l: [i.get('attr_val_id') for i in l]
            av_id_list = func(attr_val_list)
            av_obj_list = AttributeVal.query.filter(AttributeVal.id.in_(av_id_list)).all()
            ak = AttributeKey.query.get(attr_key_id)
            if ak and len(av_obj_list) == len(attr_val_list):
                ak.prod_category_id = category_id
                ak.product_id = product_id
                ak.name = attr_key
                db.session.commit()

                for _av in attr_val_list:
                    av = AttributeVal.query.get(int(_av.get('attr_val_id')))
                    if int(av.attr_key_id) == ak.id:
                        av.name = _av.get('attr_val')
                    else:
                        ab_code_2(1000001)
                db.session.commit()
            else:
                ab_code_2(1000001)

            return api_result(code=200, message='操作成功', data=data)
        else:
            ab_code_2(1000001)


def create_query():
    pass


class SkuPageApi(Resource):
    """
    sku page
    """

    def post(self):
        data = request.get_json()
        q = data.get('q')
        max_price = data.get('max_price')
        min_price = data.get('min_price')
        max_cost_price = data.get('max_cost_price')
        min_cost_price = data.get('min_cost_price')
        max_sale_price = data.get('max_sale_price')
        min_sale_price = data.get('min_sale_price')
        page, size = page_size(**data)

        # Todo
        sql = """
        SELECT
        -- *,
        pro.id,
        pro.name,
        sku.id,
        sku.icon,
        sku.spec,
        sku.price,
        sku.cost_price,
        sku.sale_price,
        sku.create_time,
        sku.update_time,
        sku.remark
        FROM ec_sku as sku LEFT JOIN ec_product as pro ON sku.product_id=pro.id 
        WHERE (pro.name LIKE"%{}%" or sku.spec LIKE"%{}%") 
        ORDER BY sku.create_timestamp LIMIT {},{};
        """.format(q, q, page, size)

        like_list = [
            Sku.remark.ilike("%{}%".format(q if q else '')),
        ]
        where_list = [
            # Sku.remark == 'yyx'
        ]
        where_list.append(
            Sku.price.between(max_price, min_price)) if max_price and min_price else None
        where_list.append(
            Sku.cost_price.between(max_cost_price, min_cost_price)) if max_cost_price and min_cost_price else None
        where_list.append(
            Sku.sale_price.between(max_sale_price, min_sale_price)) if max_sale_price and min_sale_price else None

        result = Sku.query.filter(or_(*like_list), *where_list).order_by(Sku.create_time.desc())
        pagination = result.paginate(page=int(page), per_page=int(size), error_out=False)
        result_list = [r.to_json() for r in pagination.items]
        return api_result(code=200, message='操作成功', data=result_list)
