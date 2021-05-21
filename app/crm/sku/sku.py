# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 下午1:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : sku.py
# @Software: PyCharm


from app.all_reference import *
from app.models.product.models import Product, AttributeKey, AttributeVal, Sku


class SkuApi(Resource):
    """
    sku api
    GET: sku详情
    POST: sku新增
    PUT: sku编辑
    DELETE: sku删除
    """

    def get(self, sku_id=None):
        sku_obj = Sku.query.get(sku_id)
        if sku_obj:
            return api_result(code=200, message='操作成功', data=sku_obj.to_json())
        else:
            ab_code_2(1000001)

    def post(self):
        data = request.get_json()
        attr_list = data.get('attr_list', [])
        if attr_list and isinstance(attr_list, list):
            for attr in attr_list:
                attr_val = attr.get('attr_val', [])
                if attr_val:
                    prod_category_id = attr.get('category_id', 0) if attr.get('category_id', 0) else 0
                    product_id = attr.get('product_id') if attr.get('product_id') else 0
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
            return api_result(code=201, message='操作成功', data=data)
        else:
            ab_code_2(1000001)

    def put(self):
        data = request.get_json()
        attr_key_id = int(data.get('attr_key_id', 0))
        category_id = data.get('category_id') if data.get('category_id') else 0
        product_id = data.get('product_id') if data.get('product_id') else 0
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
                # Todo 更新人
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

            return api_result(code=203, message='操作成功', data=data)
        else:
            ab_code_2(1000001)

    def delete(self, sku_id=None):
        sku_obj = Sku.query.get(sku_id)
        if sku_obj:
            sku_obj.is_deleted = sku_obj.id
            db.session.commit()
            return api_result(code=204, message='操作成功', data=[])
        else:
            ab_code_2(1000001)


class SkuPageApi(Resource):
    """
    sku page api
    POST: sku分页模糊查询
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

        sql_demo = """
        SELECT
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
        WHERE (
        pro.id LIKE"%iphone%" 
        or pro.name LIKE"%iphone%" 
        or sku.id LIKE"%iphone%" 
        or sku.spec LIKE"%iphone%" 
        or sku.remark LIKE"%iphone%"
        ) 
        and sku.is_deleted=0
        and (sku.price BETWEEN 10 and 40) 
        and (sku.price BETWEEN 10 and 40) 
        and (sku.cost_price BETWEEN 1 and 2) 
        and (sku.sale_price BETWEEN 100 and 200)
        ORDER BY sku.create_timestamp LIMIT 0,20;
        """

        like_list = [
            Sku.id.ilike("%{}%".format(q if q else '')),
            Sku.spec.ilike("%{}%".format(q if q else '')),
            Sku.remark.ilike("%{}%".format(q if q else '')),
            Product.id.ilike("%{}%".format(q if q else '')),
            Product.name.ilike("%{}%".format(q if q else ''))
        ]
        where_list = [
            Sku.is_deleted == 0
        ]
        where_list.append(
            Sku.price.between(max_price, min_price)) if max_price and min_price else None
        where_list.append(
            Sku.cost_price.between(max_cost_price, min_cost_price)) if max_cost_price and min_cost_price else None
        where_list.append(
            Sku.sale_price.between(max_sale_price, min_sale_price)) if max_sale_price and min_sale_price else None

        result = Sku.query.join(
            Product,
            Sku.product_id == Product.id
        ).filter(
            or_(*like_list),
            *where_list
        ).with_entities(
            Sku, Product
        ).order_by(
            Sku.create_time.desc()
        ).paginate(
            page=int(page),
            per_page=int(size),
            error_out=False
        )

        result_list = []
        for res in result.items:
            print(res)
            sku_json = res[0].to_json()
            product_json = res[1].to_json()
            sku_json['product_json'] = product_json
            result_list.append(sku_json)

        return api_result(code=200, message='操作成功', data=result_list)
