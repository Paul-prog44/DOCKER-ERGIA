import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environments';


@Injectable({
  providedIn: 'root'
})
export class CorpusService {
  private apiUrl = environment.apiUrl

  constructor(private http: HttpClient) { }

  getTexts(text_id :  number): Observable<any> {
    return this.http.get(`${this.apiUrl}/text/${text_id}`)
  }

  getSummaries(summary_id : number): Observable<any> {
    return this.http.get(`${this.apiUrl}/summary/${summary_id}`)
  }

  getTextsByCampaign(campaign_id: number):Observable<any> {
    return this.http.get(`${this.apiUrl}/texts/${campaign_id}`)
  }

  getSummariesByOriginalText(original_text_id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/summaries/${original_text_id}`)
  }
}
