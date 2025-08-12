/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PaymentScreen.prototype, {
    setup(){
        super.setup()
        this.orm = useService('orm')
    },
    async _isOrderValid(){
        const result = super._isOrderValid()
        var payment_method =  this.paymentLines.some(paymentLines =>{
        return paymentLines.payment_method_id.is_ledger
        });
        if (payment_method){
            var due = (this.paymentLines.find(paymentLines =>{
            return paymentLines.payment_method_id.is_ledger})).amount
            if (this.currentOrder.get_partner()){
                const partner = this.currentOrder.get_partner().id;
                const balance = await this.orm.call(
                "res.partner","get_remaining_amount",[partner],);
                if (balance >=due){
                    const remaining_amount = await this.orm.call(
                    "res.partner","update_remaining_due",[partner,due],);
                    return result
                }
                else if(balance == false){
                    this.dialog.add(AlertDialog, {
                    title: "Invalid",
                    body: "Credit is not allowed for the user..."});
                }
                else{
                    this.dialog.add(AlertDialog, {
                    title: "Wallet Empty",
                    body: "Please change the payment Method Remaining balance " + balance});
                }
            }
            else{
                    this.dialog.add(AlertDialog, {
                    title: "Customer Required",
                    body: "Customer is Required for using Credit Account..."});
            }
        }
        else{
        return result
        }
    },
});
