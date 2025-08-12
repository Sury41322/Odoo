/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { WarningDialog } from "@web/core/errors/error_dialogs";
import { Component } from "@odoo/owl";
import {Dropdown} from '@web/core/dropdown/dropdown';
import { rpc } from "@web/core/network/rpc";
import {  useState } from "@odoo/owl";

const Weather_icons = {
"clear" : "/weather_icon/static/src/img/clear.png",
"clouds": "/weather_icon/static/src/img/few_clouds.png",
"rain": "/weather_icon/static/src/img/rain.png",
"thunderstorm" : "/weather_icon/static/src/img/thunderstorm.png",
"snow" : "/weather_icon/static/src/img/snow.png",
"mist" : "/weather_icon/static/src/img/mist.png"
}
class SystrayIcon extends Component {
    setup() {
       super.setup(...arguments);
       this.dialogService = useService("dialog");
       this.state = useState({
            weather : null,
            coords : null,
            time : null,
            icon : null,
       })
    }
    _get_location() {
        return new Promise((resolve ,reject) = >
        {
        if (!navigator.geolocation){
            return reject("Error Geolocation Not Available")
        }
        else{
            navigator.geolocation.getCurrentPosition(
            (pos)=>{
                const crd = pos.coords;
                 resolve({"latitude" : crd.latitude,
                          "longitude" : crd.longitude})
            })
            }
        })
    }
    async _onClick() {
        this.state.time = new Date(Date.now()).toLocaleString()
        const coords = await this._get_location()
        this.state.coords = coords
        this.state.weather = await this.get_weather_data()
        this.state.icon = Weather_icons[(this.state.weather.weather[0].main).toLowerCase()]
    }
    async get_weather_data(){
        const result = await rpc("/weather/status",
        {lat : this.state.coords['latitude'],
         long : this.state.coords['longitude']
        });
        return result
    }
    async _on_submit(){
        var elm = document.getElementById("place").value
        if (!elm){
            this.dialogService.add(WarningDialog, {
                title: "Warning: Invalid Search Value",
                message: "Search Value Cannot be Empty...",
            });
        }
        else{
            const result = await rpc("/weather/status",
                {place : elm });
            if (result.message == "city not found"){
                this.dialogService.add(WarningDialog, {
                title: "Warning: City not Found",
                message: "city , country-code",
            });
            }
            else{
                this.state.weather = result
                this.state.icon = Weather_icons[(result.weather[0].main).toLowerCase()]
            }
        }
    }
}
SystrayIcon.template = "weather_icon";
SystrayIcon.components = {Dropdown };
export const systrayItem = {
    Component: SystrayIcon,
};
registry.category("systray").add("SystrayIcon", systrayItem);
