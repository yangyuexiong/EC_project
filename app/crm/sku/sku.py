# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 下午1:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : sku.py
# @Software: PyCharm


from app.all_reference import *
from app.models.product.models import AttributeKey, AttributeVal, Sku, ProductStock


class SkuApi(Resource):
    """
    sku
    """

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
