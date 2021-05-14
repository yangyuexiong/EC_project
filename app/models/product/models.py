# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午6:20
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from ExtendRegister.db_register import db
from common.libs.BaseModel import BaseModel


class ProductBrand(BaseModel):
    __tablename__ = 'ec_brand'
    __table_args__ = {'comment': '品牌'}
    name = db.Column(db.String(64), nullable=False, comment='品牌名称')
    parent_id = db.Column(db.Integer, nullable=True, comment='上级分类的编号:0表示一级分类')
    level = db.Column(db.Integer, nullable=True, comment='分类级别:0->1级;1->2级')
    nav_status = db.Column(db.Integer, nullable=True, comment='是否显示在导航栏:0-不显示;1-显示')
    show_status = db.Column(db.Integer, nullable=True, comment='显示状态:0-不显示;1-显示')
    sort = db.Column(db.Integer, nullable=True, comment='排序')
    icon = db.Column(db.String(255), nullable=True, comment='图标')
    keywords = db.Column(db.String(255), nullable=True, comment='关键字')
    create_user_id = db.Column(db.String(32), nullable=True, comment='创建人id')
    create_username = db.Column(db.String(32), nullable=True, comment='创建人')
    update_user_id = db.Column(db.String(32), nullable=True, comment='更新人id')
    update_username = db.Column(db.String(32), nullable=True, comment='更新人')
    remark = db.Column(db.String(255), nullable=True, comment='备注')

    def __repr__(self):
        return 'ProductBrand 模型对象-> ID:{} 品牌名称:{}'.format(self.id, self.name)


class ProductCategory(BaseModel):
    __tablename__ = 'ec_product_category'
    __table_args__ = {'comment': '商品类目'}
    name = db.Column(db.String(64), nullable=False, comment='类目名称')
    parent_id = db.Column(db.Integer, nullable=True, comment='上级分类的编号:0表示一级分类')
    level = db.Column(db.Integer, nullable=True, comment='分类级别:0->1级;1->2级')
    nav_status = db.Column(db.Integer, nullable=True, comment='是否显示在导航栏:0-不显示;1-显示')
    show_status = db.Column(db.Integer, nullable=True, comment='显示状态:0-不显示;1-显示')
    sort = db.Column(db.Integer, nullable=True, comment='排序')
    icon = db.Column(db.String(255), nullable=True, comment='图标')
    keywords = db.Column(db.String(255), nullable=True, comment='关键字')
    create_user_id = db.Column(db.String(32), nullable=True, comment='创建人id')
    create_username = db.Column(db.String(32), nullable=True, comment='创建人')
    update_user_id = db.Column(db.String(32), nullable=True, comment='更新人id')
    update_username = db.Column(db.String(32), nullable=True, comment='更新人')
    remark = db.Column(db.String(255), nullable=True, comment='备注')

    def __repr__(self):
        return 'ProductCategory 模型对象-> ID:{} 商品类目名称:{}'.format(self.id, self.name)


class Product(BaseModel):
    __tablename__ = 'ec_product'
    __table_args__ = {'comment': '商品'}
    prod_category_id = db.Column(db.String(64), nullable=True, comment='商品类目id')
    name = db.Column(db.String(64), nullable=False, comment='商品名称')
    subtitle = db.Column(db.String(64), nullable=True, comment='副标题')
    summary = db.Column(db.String(255), nullable=True, comment='商品简介')
    price = db.Column(db.DECIMAL(10, 2), nullable=True, default=0, comment='销售价')
    cost_price = db.Column(db.DECIMAL(10, 2), nullable=True, default=0, comment='成本价')
    sale_price = db.Column(db.DECIMAL(10, 2), nullable=True, default=0, comment='促销价')
    sale_status = db.Column(db.String(16), default='1', comment='销售状态:1-正常;2-推荐;3-热销')
    prod_status = db.Column(db.String(16), default='1', comment='商品状态:1-已上架;2-已下架;3-待审核;4-待上架;5-审核不通过;')
    cover_picture = db.Column(db.String(255), nullable=True, comment='封面图片')
    video = db.Column(db.String(255), nullable=True, comment='视频')
    carousel = db.Column(db.JSON, nullable=True, comment='轮播图')
    image_link_dict = db.Column(db.JSON, nullable=True, comment='图片')
    attr_json = db.Column(db.JSON, nullable=True, comment='attr json')
    create_user_id = db.Column(db.String(32), nullable=True, comment='创建人id')
    create_username = db.Column(db.String(32), nullable=True, comment='创建人')
    update_user_id = db.Column(db.String(32), nullable=True, comment='更新人id')
    update_username = db.Column(db.String(32), nullable=True, comment='更新人')
    remark = db.Column(db.String(255), nullable=True, comment='备注')

    def __repr__(self):
        return 'Product 模型对象-> ID:{} 商品:{}'.format(self.id, self.name)


class AttributeKey(BaseModel):
    __tablename__ = 'ec_attr_key'
    __table_args__ = {'comment': '属性名'}
    prod_category_id = db.Column(db.String(64), nullable=True, comment='商品类目id')
    product_id = db.Column(db.String(64), nullable=True, comment='商品id')
    name = db.Column(db.String(64), nullable=True, comment='属性名称')
    create_user_id = db.Column(db.String(32), nullable=True, comment='创建人id')
    create_username = db.Column(db.String(32), nullable=True, comment='创建人')
    update_user_id = db.Column(db.String(32), nullable=True, comment='更新人id')
    update_username = db.Column(db.String(32), nullable=True, comment='更新人')
    remark = db.Column(db.String(255), nullable=True, comment='备注')

    def __repr__(self):
        return 'AttributeKey 模型对象-> ID:{} 属性名:{} 商品类目id:{}'.format(self.id, self.name, self.prod_category_id)


class AttributeVal(BaseModel):
    __tablename__ = 'ec_attr_val'
    __table_args__ = {'comment': '属性值'}
    attr_key_id = db.Column(db.String(64), nullable=True, comment='属性名key_id')
    name = db.Column(db.String(64), nullable=True, comment='属性值名称')
    create_user_id = db.Column(db.String(32), nullable=True, comment='创建人id')
    create_username = db.Column(db.String(32), nullable=True, comment='创建人')
    update_user_id = db.Column(db.String(32), nullable=True, comment='更新人id')
    update_username = db.Column(db.String(32), nullable=True, comment='更新人')
    remark = db.Column(db.String(255), nullable=True, comment='备注')

    def __repr__(self):
        return 'AttributeVal 模型对象-> ID:{} 属性值:{} 属性名key_id:{}'.format(self.id, self.name, self.attr_key_id)


class Sku(BaseModel):
    __tablename__ = 'ec_sku'
    __table_args__ = {'comment': '商品规格/库存'}
    product_id = db.Column(db.String(64), nullable=True, comment='商品id')
    icon = db.Column(db.String(64), nullable=True, comment='icon')
    spec = db.Column(db.JSON, nullable=True, comment='商品规格Json')
    price = db.Column(db.DECIMAL(10, 2), nullable=True, default=0, comment='销售价')
    cost_price = db.Column(db.DECIMAL(10, 2), nullable=True, default=0, comment='成本价')
    sale_price = db.Column(db.DECIMAL(10, 2), nullable=True, default=0, comment='促销价')
    remark = db.Column(db.String(255), nullable=True, comment='备注')

    def __repr__(self):
        return 'Sku 模型对象-> ID:{} 商品规格:{} 库存:{} 金额:{}'.format(
            self.id, self.commodity_spec, self.stock, self.price
        )


class ProductComment(BaseModel):
    __tablename__ = 'ec_product_comment'
    __table_args__ = {'comment': '商品评论'}
    user_id = db.Column(db.String(64), nullable=True, comment='用户id')
    product_id = db.Column(db.String(64), nullable=True, comment='商品id')
    content = db.Column(db.String(1024), nullable=True, comment='内容')
    star = db.Column(db.String(64), nullable=True, comment='星星')
    image_link_dict = db.Column(db.JSON, nullable=True, comment='图片')
    remark = db.Column(db.String(255), nullable=True, comment='备注')

    def __repr__(self):
        return 'ProductComment 模型对象-> ID:{} 用户:{} 商品:{}'.format(
            self.id, self.user_id, self.commodity_id
        )


class ProductStock(BaseModel):
    __tablename__ = 'ec_stock'
    __table_args__ = {'comment': '商品库存'}
    product_id = db.Column(db.String(64), nullable=True, comment='商品id')
    sku_id = db.Column(db.String(64), nullable=True, comment='sku-id')
    stock = db.Column(db.Integer, nullable=True, comment='库存')

    def __repr__(self):
        return 'ProductStock 模型对象-> ID:{} 商品id:{} sku_id:{} 库存:{}'.format(
            self.id, self.product_id, self.sku_id, self.stock
        )


class ProductSales(BaseModel):
    __tablename__ = 'ec_sales'
    __table_args__ = {'comment': '商品销量'}
    product_id = db.Column(db.String(64), nullable=True, comment='商品id')
    sku_id = db.Column(db.String(64), nullable=True, comment='sku-id')
    sales = db.Column(db.Integer, nullable=True, comment='销量')

    def __repr__(self):
        return 'ProductStock 模型对象-> ID:{} 商品id:{} sku_id:{} 销量:{}'.format(
            self.id, self.product_id, self.sku_id, self.sales
        )


class ProductOperationLog(BaseModel):
    __tablename__ = 'ec_prod_operation_log'
    __table_args__ = {'comment': '商品操作记录'}
    product_id = db.Column(db.String(64), nullable=True, comment='商品id')
    op_user_id = db.Column(db.String(32), nullable=True, comment='操作人id')
    op_username = db.Column(db.String(32), nullable=True, comment='操作人名称')
    op_type = db.Column(db.String(16), nullable=True, comment='操作类型:1-新增;2-删除;3-修改')
    field = db.Column(db.String(128), nullable=True, comment='操作字段名称')
    before_val = db.Column(db.String(32), nullable=True, comment='修改前的值')
    after_val = db.Column(db.String(32), nullable=True, comment='修改后的值')

    def __repr__(self):
        return 'ProductOperationLog 模型对象-> ID:{} 商品id:{} 用户id:{} 用户名称:{}'.format(
            self.id, self.product_id, self.user_id, self.username
        )
