/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import { registry } from "@web/core/registry";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

        publicWidget.registry.latest_property_snippet = publicWidget.Widget.extend({
            selector: '.property_div',
            start: function () {
                     this.snippetFunction();
            },
            snippetFunction: async function(){
            const result = await rpc('/get_latest_property', {});
            var chunks = await this.chunk(result['property'], 4);
            chunks[0].is_active = true
            this.$target.empty().html(renderToElement('property_management.property_data', {chunks:chunks}))
            },
            chunk : async function(array , size){
            const chunkedArray =[]
            for (let i =0 ;i<array.length; i+= size)
                {
                    chunkedArray.push(array.slice(i,i+size))
                }
            return chunkedArray
            }
        });
