/** @odoo-module **/
import { registry } from "@web/core/registry";
import publicWidget from "@web/legacy/js/public/public_widget";
publicWidget.registry.PropertyManagement = publicWidget.Widget.extend({
   selector: ".property_form",
   events: {
        'change input[name="type"]' : '_onChangeType',
       'change #property' : '_onChangeProperty',
       'click .add_total_project': '_onClickAdd_total_project',
       'click .remove_line': '_onClickRemoveLine',
       'click .submit': '_onClickSubmit',
   },
   init() {
   this.orm = this.bindService("orm");
   },
   _onClickSubmit: async function(ev){
     var self = this;
           var tenant = $('#tenant_id').data('id')
           var date = $('#end_date').val()
           var type = $('input[name=type]:checked').val()
           var property_data = [];
           var rows = $(
               '#property_table > tbody > tr.property_order_line');
           for(var i=0;i<rows.length;i++){
           var values=rows[i]
               let property = $(values).find('#property').val();
               let amount = $(values).find("#amount").text();
               if (property != ""){
               property_data.push({
                       'property':property,
                       'amount':parseFloat(amount),
               });
               }
               }
               if (date == "" || property_data.length==0){
               $("#alert").removeClass("d-none")
               }
               else{
               await this.orm.call('rental.lease.management',
               'create_record',
               [tenant,
               date,
               type,
               property_data],)
               window.location.href ="/order_webform/submit"
               }
    },
    _onChangeProperty: async function(ev){
        var property_id = $(ev.target)
       var type = $('input[name=type]:checked').val()
        const result = await this.orm.call('property.management',
        'get_values',
        [parseInt(property_id.val()),
        type],)
        property_id.closest('tr').find('.owner').html(result[0])
        property_id.closest('tr').find('.amount').html
        ("<span id=amount name=legal value=" + result[1] + ">" + result[1]+ "</span>")
    },
    _onChangeType : async function(ev){
    var rows = $(
               '#property_table > tbody > tr.property_order_line');
                    for(var i=0;i<rows.length;i++){
                        var property_id = $(rows[i]).find("#property")
                         if (property_id.val() != ""){
                            const result = await this.orm.call('property.management',
                            'get_values',
                            [parseInt($(rows[i]).find("#property").val()),
                            $(ev.target).val()])
                            property_id.closest('tr').find('.amount').html("<span id=amount name=legal value=" + result[1] + ">" + result[1] + "</span>")
                         }
                    }
    },
   _onClickAdd_total_project: function(ev){
               var $new_row = $('.add_extra_property').clone(true);
               $new_row.removeClass('d-none');
               $new_row.removeClass('add_extra_property');
               $new_row.addClass('property_order_line');
               $new_row.insertBefore($('.add_extra_property'));
    },
    _onClickRemoveLine : function(ev){
                var rows = $(
               '#property_table > tbody > tr.property_order_line');
               if (rows.length >1){
               $(ev.target).parent().parent().remove()
               }
    },
   });