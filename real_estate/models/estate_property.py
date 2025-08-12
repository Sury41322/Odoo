
from odoo import models,fields,api
from datetime import timedelta
from odoo.fields import Date

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model For the Properties of the Estate (fields and Attributes)."

    tag_ids=fields.Many2many("estate.property.tags" ,string="Tags")
    name = fields.Char(string="Estate Name" , required=True)
    image = fields.Binary(string="Image")
    property_type = fields.Many2one("estate.property.type"  ,string="Property Type")
    description = fields.Char(compute="_description_text" ,store=True)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Datetime(copy=False)
    expected_price = fields.Float(required = True)
    bedrooms = fields.Integer()
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean(compute="_inverse_onchange_garden" , inverse="_onchange_garden")
    garden_area = fields.Integer(string="Garden Area(sqm)",compute="_onchange_garden", inverse="_inverse_onchange_garden")
    garden_orientation = fields.Selection(
        [("North","North"),("South","South"),("East","East"),("West","West")],
        compute="_onchange_garden", inverse="_inverse_onchange_garden")
    active = fields.Boolean(default="True")
    status = fields.Selection([("New","New"),("Offer_Received","Offer Received"),("Offer_Accepted","Offer Accepted"),("Sold","Sold"),("Cancelled","Cancelled")] ,default="New", required=True , copy=False)
    salesman = fields.Many2one("res.users",string="Sales Person" , default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner" , string="Buyer" , readonly=True)
    offers = fields.One2many("estate.property.offer" , "property_id" ,string=" " )
    total_area = fields.Float(compute="_total_area")
    best_offer = fields.Float(compute="_best_offer")
    selling_price = fields.Float( readonly=True,copy=False)

    def action_sold(self):
        if self.status != "Cancelled":
            self.write({'status':'Sold'})
        else:
            raise UserWarning("Already Cancelled")

    def action_cancel(self):
        if self.status != "Sold":
            self.write({'status':"Cancelled"})
        else:
            raise  UserWarning("Already Sold")

    @api.depends("living_area","garden_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _best_offer(self):
        for record in self:
            if record.offers:
                record.best_offer = max(record.offers.mapped("price"))
            else:
                record.best_offer = 0
                # if line.price > record.best_offer:
                #     record.best_offer = line.price


    @api.depends("property_type.name")
    def _description_text(self):
        for record in self:
            record.description ="New Offer for %s is been listed " % record.property_type.name


    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden :
                record.garden_area=record.garden_area =10
                record.garden_orientation="North"
            else:
                record.garden_area =0
                record.garden_orientation = ""

    @api.onchange("garden_area","garden_orientation")
    def _inverse_onchange_garden(self):
        pass
        # for record in self:
        #     if record.garden_area == 0 or record.garden_orientation == "":
        #         record.garden = False
        #     else :
        #         record.garden = True

    # def _inverse_onchange_garden(self):
    #     for record in self:
    #         record.garden("")

    @api.depends("offers")
    def _sample_231(self):
        for record in self:
            for line in record.offers:
                print(line.price)


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float()
    status = fields.Selection([
        ("Accepted", "Accepted"), ("Rejected", "Rejected")
    ], copy=False)
    create_date = fields.Date(compute="_create_date")
    validity = fields.Integer(compute="_inverse_validity", inverse="_validity")
    date_deadline = fields.Date(string="Expiry Date", compute="_validity", inverse="_inverse_validity")
    partner_id = fields.Many2one("res.partner", string="Partner Name")
    property_id = fields.Many2one("estate.property", string="Property Name")

    def is_accepted(self):
        for record in self:
            record.status= "Accepted"



    def is_rejected(self):
        for record in self:
            record.status = "Rejected"


    def _create_date(self):
            self.create_date = Date.today()

    @api.depends("validity","create_date")
    def _validity(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    @api.depends( "date_deadline","create_date")
    def _inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline- record.create_date).days
            if record.validity < 0 :
                raise Warning("Entered Expiry date is less than creation date")