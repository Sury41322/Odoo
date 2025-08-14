/** @odoo-module **/
import { registry } from "@web/core/registry";
import { loadBundle } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component , useState ,onWillStart ,useEffect } from "@odoo/owl";
const actionRegistry = registry.category("actions");
class CrmDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.state = useState({
            type : 'create_date',
            my_leads : 0,
            my_opportunity : 0,
            revenue : 0,
            user_revenue : 0,
            ratio : 0,
            won_amount : 0,
            lost_amount : 0
       });
        this._fetch_data();
        this.line_chart = null
        this.pie_chart = null
        this.doughnut_chart = null
        onWillStart(async () => await loadBundle("web.chartjs_lib"));
//        this.renderChart()
//        this.renderChart()
useEffect(() => {
            this.renderChart();
            return () => {
                if (this.line_chart || this.pie_chart || this.doughnut_chart) {
                    this.line_chart.destroy();
                    this.pie_chart.destroy();
                    this.doughnut_chart.destroy();
                }
//                this.renderChart()
            };
        });

//        useEffect(() => {
//            this.renderChart();
//            return () => {
//            this.chart.destroy()
//            };
//        });
  }
  async _fetch_data(){
     let result = await this.orm.call("crm.lead", "get_tiles_data", [], {});
     this.set_data(result)

  }
  set_type(ev){
    this.state.type= ev.target.value
  }
  async set_period(ev){
    let result = await this.orm.call("crm.lead", "get_tiles_data", [ev.target.value , this.state.type], {});
    this.set_data(result)
  }
  set_data(result){
        this.state.my_leads = result.total_leads,
        this.state.my_opportunity = result.total_opportunity,
        this.state.revenue = result.expected_revenue,
        this.state.user_revenue = result.revenue,
        this.state.ratio = result.win_ratio,
        this.state.won_amount = result.won_amount,
        this.state.lost_amount = result.lost_amount
  }
  renderChart(){
   this.line_chart = new Chart("line_chart", {
    type: "line",
    data: {
        labels: [10, 20, 30, 40, 50],
        datasets: [{
            data: [10, 20, 30, 40, 50],
            pointBackgroundColor: "black",
        }]
    },
    option: {}
});
 this.pie_chart = new Chart("pie_chart", {
    type: "pie",
    data: {
        datasets: [{
            backgroundColor: "red",
            data: [0, 10, 20, 30, 40]
        }]
    },
    options: {}
});
this.doughnut_chart = new Chart("doughnut_chart", {
    type: "doughnut",
    data: {
        datasets: [{
            backgroundColor: "purple",
            data: [0, 10, 20, 30, 40]
        }]
    },
    options: {
    }
});
}
}
CrmDashboard.template = "crm_lead.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);