# -*- coding: utf-8 -*-
# @Time    : 2021/5/28 下午5:22
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class Order(BaseModel):
    __tablename__ = 'ec_order'
    __table_args__ = {'comment': '订单表'}
    order_number = db.Column(db.String(128), unique=True, comment='订单号')
    out_order_number = db.Column(db.String(128), comment='第三方订单号')
    user_id = db.Column(BIGINT(20, unsigned=True), comment='用户id')
    mobile = db.Column(db.String(64), comment='用户手机号')
    user_remark = db.Column(db.String(128), comment='用户备注')
    total_amount = db.Column(db.DECIMAL(10, 2), comment='订单总金额')
    pay_amount = db.Column(db.DECIMAL(10, 2), comment='应付金额(实际支付金额)')
    freight_amount = db.Column(db.DECIMAL(10, 2), comment='运费金额')
    promotion_amount = db.Column(db.DECIMAL(10, 2), comment='促销优化金额(促销价、满减、阶梯价)')
    integration_amount = db.Column(db.DECIMAL(10, 2), comment='积分抵扣金额')
    coupon_amount = db.Column(db.DECIMAL(10, 2), comment='优惠券抵扣金额')
    discount_amount = db.Column(db.DECIMAL(10, 2), comment='管理员后台调整订单使用的折扣金额')
    pay_type = db.Column(TINYINT(1, unsigned=True), comment='支付方式:0->未支付;1->支付宝;2->微信')
    source_type = db.Column(TINYINT(1, unsigned=True), comment='订单来源:0->PC订单;1->app订单')
    order_type = db.Column(TINYINT(1, unsigned=True), comment='订单类型:0->正常订单;1->秒杀订单')
    order_status = db.Column(TINYINT(1, unsigned=True), comment='订单状态:0->待付款;1->待发货;2->已发货;3->已完成;4->已关闭;5->退费中;6->已退费')
    integration = db.Column(BIGINT(20, unsigned=True), comment='可以获得的积分')
    growth = db.Column(BIGINT(20, unsigned=True), comment='可以获得的成长值')
    payment_time = db.Column(db.DateTime, comment='支付时间')
    delivery_company = db.Column(db.String(128), comment='物流公司(配送方式)')
    delivery_sn = db.Column(db.String(256), comment='物流单号')
    receiver_name = db.Column(db.String(128), comment='收货人姓名')
    receiver_phone = db.Column(db.String(128), comment='收货人电话')
    receiver_post_code = db.Column(db.String(128), comment='收货人邮编')
    receiver_province = db.Column(db.String(128), comment='省份/直辖市')
    receiver_city = db.Column(db.String(128), comment='城市')
    receiver_region = db.Column(db.String(128), comment='区')
    receiver_detail_address = db.Column(db.String(512), comment='详细地址')
    delivery_time = db.Column(db.DateTime, comment='发货时间')
    confirm_status = db.Column(TINYINT(1, unsigned=True), comment='确认收货状态:0->未确认;1->已确认')
    auto_confirm_day = db.Column(TINYINT(1, unsigned=True), server_default='14', comment='自动确认时间(天)')
    receive_time = db.Column(db.DateTime, comment='确认收货时间')
    bill_type = db.Column(TINYINT(1, unsigned=True), comment='发票类型:0->不开发票;1->电子发票;2->纸质发票')
    bill_header = db.Column(db.String(256), comment='发票抬头')
    bill_content = db.Column(db.String(256), comment='发票内容')
    bill_receiver_email = db.Column(db.String(256), comment='收票人邮箱')

    def __repr__(self):
        return 'Order 模型对象-> ID:{} 订单号:{} 用户id:{}'.format(
            self.id, self.order_number, self.user_id
        )


class OrderItem(BaseModel):
    __tablename__ = 'ec_order_item'
    __table_args__ = {'comment': '订单商品信息表'}
    user_id = db.Column(BIGINT(20, unsigned=True), comment='用户id')
    order_id = db.Column(BIGINT(20, unsigned=True), comment='订单id')
    order_number = db.Column(db.String(128), comment='订单号')
    product_quantity = db.Column(BIGINT(20, unsigned=True), comment='购买数量')
    product_category_id = db.Column(BIGINT(20, unsigned=True), comment='商品分类id')
    product_brand = db.Column(db.String(128), unique=True, comment='商品品牌')
    product_id = db.Column(BIGINT(20, unsigned=True), comment='商品id')
    product_name = db.Column(db.String(128), comment='商品名称')
    product_pic = db.Column(db.String(1024), comment='商品图片')
    product_sku_id = db.Column(BIGINT(20, unsigned=True), comment='商品sku编号')
    product_sku_spec = db.Column(db.JSON, comment='商品规格Json')
    product_price = db.Column(db.DECIMAL(10, 2), comment='销售价格')
    real_amount = db.Column(db.DECIMAL(10, 2), comment='该商品经过优惠后的分解金额')
    coupon_amount = db.Column(db.DECIMAL(10, 2), comment='优惠券优惠分解金额')
    promotion_amount = db.Column(db.DECIMAL(10, 2), comment='商品促销分解金额')
    integration_amount = db.Column(db.DECIMAL(10, 2), comment='积分优惠分解金额')
    gift_growth = db.Column(BIGINT(20, unsigned=True), comment='商品赠送成长值')
    gift_integration = db.Column(BIGINT(20, unsigned=True), comment='商品赠送积分')

    def __repr__(self):
        return 'OrderItem 模型对象-> ID:{} 订单号:{} 用户id:{} 商品id:{} sku_id:{}'.format(
            self.id, self.order_number, self.user_id, self.product_id, self.product_sku_id
        )


class OrderSnapshot(BaseModel):
    __tablename__ = 'ec_order_snapshot'
    __table_args__ = {'comment': '订单快照表'}
    caption = db.Column(db.String(128), comment='标题')
    user_id = db.Column(BIGINT(20, unsigned=True), comment='用户id')
    order_id = db.Column(BIGINT(20, unsigned=True), comment='订单id')
    order_number = db.Column(db.String(128), comment='订单号')
    order_info = db.Column(db.JSON, comment='订单信息json')

    def __repr__(self):
        return 'OrderSnapshot 模型对象-> ID:{} 订单id:{} 订单号:{} 用户id:{}'.format(
            self.id, self.order_id, self.order_number, self.user_id
        )
