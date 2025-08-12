/** @odoo-module */
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { patch } from "@web/core/utils/patch";

patch(ProductCard.prototype, {
   get Rating(){
        if (this.props.product.pos_rating == false){
            return 0
            }
        else{
        return this.props.product.pos_rating
        }
   }
});
