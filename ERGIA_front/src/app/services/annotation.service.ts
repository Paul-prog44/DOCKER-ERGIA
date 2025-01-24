import { Injectable } from '@angular/core';
import { environment } from '../environments/environments';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {Annotation } from '../../api/models/annotation'

@Injectable({
  providedIn: 'root'
})
export class AnnotationService {
  private apiUrl = environment.apiUrl

  constructor(private http : HttpClient) { }

  createAnnotation(data : Annotation[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/annotations`, data)
  }

  getAnnotations(resumeId : number): Observable<Annotation[]> {
    return this.http.get<Annotation[]>(`${this.apiUrl}/synthese/${resumeId}/annotations/`)
  }

  deleteAnnotation(annotationId : number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/synthese/annotations/${annotationId}`)
  }
}
