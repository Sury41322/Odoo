/** @odoo-module */
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
   getDisplayData() {
   const result = super.getDisplayData()
   if (this.product_id.pos_rating){
   result.receipt_pos_rating = this.product_id.pos_rating
   }
   else{
   result.receipt_pos_rating = '0'
   }
   return result
   },
});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                receipt_pos_rating: { type: String, optional: true },
            },
        },
    },
});
