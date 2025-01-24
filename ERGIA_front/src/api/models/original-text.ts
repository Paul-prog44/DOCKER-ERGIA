import {Summary} from "./summary";

export class OriginalText {
  //campaignId: number;
  name: string;
  idOriginalText: number;
  path: string;
  content: string;
  summaries: Summary[];

  constructor(data: any) {
    //this.campaignId = data.campaign_id;
    this.summaries = []
    this.idOriginalText = data.text_id;
    this.path = data.path;
    this.name= "not found"
    this.content = data.content
    let nameWindows = this.path.match(/^([^\\]*\\){2}([^\\]*)/);
    let nameLinux = this.path.match(/^([^/]*\/){2}([^/]+)/);
    if(nameWindows){
      this.name = nameWindows[2];
    }
    else if(nameLinux) {
      this.name = nameLinux[2];
    }
  }
}
