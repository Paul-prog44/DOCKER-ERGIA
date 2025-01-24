export class Summary {
  //campaignId: number;
  annotator_id: number;
  content: string;
  path: string;
  id_summary: string;
  name: string;

  constructor(data: any) {

    this.annotator_id = data.annotator_id
    this.content = data.content
    this.path = data.path
    this.id_summary = data.id_summary
    this.name = "not found"

    let nameWindows = this.path.match(/\\([^\\]+)\.txt$/);
    let nameLinux = this.path.match(/\/([^/]+)\.txt$/)

    if(nameWindows){
      this.name = nameWindows[1];
    }
    else if(nameLinux){
      this.name = nameLinux[1];
    }
  }
}
