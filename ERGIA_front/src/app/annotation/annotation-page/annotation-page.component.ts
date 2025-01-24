import { Component, OnInit } from '@angular/core';
import * as mammoth from 'mammoth'
import { ModalAnnotationComponent } from "../modal-annotation/modal-annotation.component";
import { Annotation } from '../../../api/models/annotation';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { AnnotationService } from '../../services/annotation.service';
import { CorpusService } from '../../services/corpus.service';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-annotation-page',
  standalone: true,
  imports: [ModalAnnotationComponent],
  templateUrl: './annotation-page.component.html',
  styleUrl: './annotation-page.component.scss'
})
export class AnnotationPageComponent implements OnInit {
  referenceDocument: string | null = null
  errorMessage: string | null = null
  resume: string  | null = null
  annotatedText: SafeHtml = ""

  selectedText: string | null = null
  isPopupVisible =false  //TODO : A REMETTRE SUR FALSE
  index : number = 0
  length : number = 0
  id_summary_string: string | null = null
  id_summary: number = -1
  id_original_text_string: string | null = null
  id_original_text: number | null = null

  annotations: Annotation[] = []

  constructor(
    private sanitizer: DomSanitizer,
    private annotationService: AnnotationService,
    private corpusService: CorpusService,
    private route: ActivatedRoute) {}

  ngOnInit(): void {

    this.id_summary_string = this.route.snapshot.paramMap.get('id_summary')
    this.id_original_text_string = this.route.snapshot.paramMap.get('id_original_text')

    if(this.id_summary_string) {
      this.id_summary = +this.id_summary_string

      this.corpusService.getSummaries(this.id_summary).subscribe({
        next: (data:any) => {
          this.resume = data.content
        },
        error: (error) => {
          console.error('Erreur lors de la récupération des données :', error);
        }
      })

      if(this.id_original_text_string) {
        this.id_original_text = +this.id_original_text_string
        this.corpusService.getTexts(this.id_original_text).subscribe({
          next: (data: any) => {
            this.referenceDocument = data.content
          },
          error: (error) => {
            console.error('Erreur lors de la récupération des données :', error);
          }
        })
      }
    }



  }


  getSelectedText(): void {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) {
      return;
    }
    this.isPopupVisible = true;
    const range = selection.getRangeAt(0);
    const container = range.commonAncestorContainer;

    const parentElement = container.nodeType === 3 ? container.parentElement : container as HTMLElement;

    if (!parentElement) {
      return;
    }

    const textContent = parentElement.innerText;

    const selectionStart = this.getTextOffset(parentElement, range);

    this.selectedText = selection.toString();
    this.length = this.selectedText.length;
    this.index = selectionStart;
    }

  getTextOffset(parentElement: HTMLElement, range: Range): number {
    let offset = 0;

    const traverseNodes = (node: ChildNode): boolean => {
      if (node === range.startContainer) {
        offset += range.startOffset;
        return true;
      }

      if (node.nodeType === 3) {
        offset += node.textContent?.length || 0;
      }

      for (const child of Array.from(node.childNodes)) {
        if (traverseNodes(child)) {
          return true
        }
      }

      return false;
    };
    parentElement.childNodes.forEach(traverseNodes);

    return offset;
  }

  hidePopup() {
    this.isPopupVisible = false;
    }

  onAddAnnotation(annotation : Annotation): void {
    this.annotations.push(annotation)
    if (this.resume) {
      const highlitedText = this.applyAnnotations(this.resume || "", this.annotations);
      this.annotatedText = this.sanitizer.bypassSecurityTrustHtml(highlitedText);
    }
  }

  highlightSubstring(text: string, startIndex: number, length: number, color: string): string {
    if (!text || startIndex < 0 || length <= 0 || startIndex >= text.length) {
      return text
    }
    const before = text.substring(0, startIndex)
    const target = text.substring(startIndex, startIndex + length)
    const after = text.substring(startIndex + length)

    const wrappedTarget = `<span style="color: ${color};"><b>${target}</b></span>`

    return `${before}${wrappedTarget}${after}`
  }

  applyAnnotations(text: string, annotations: Annotation[]): string {
    let modifiedText = text
    let offset = 0
    annotations.forEach(annotation => {
      const adjustedIndex = annotation.index + offset
      const addedLength = `<span style="color: ${annotation.color};"><b></b></span>`.length;
      modifiedText = this.highlightSubstring(
        modifiedText,
        adjustedIndex,
        annotation.length,
        annotation.color || 'black'
      );
      offset += addedLength;
    });
    return modifiedText;
  }

  reloadCurrentPage() {
    window.location.reload();
   }

   saveAnnotation() {
    console.log("Annotation enregistrées : ", this.annotations)
    this.annotationService.createAnnotation(this.annotations).subscribe({
      next: (data: any) => {
        console.log(data)
      },
      error : (error) => {
        console.error('Erreur lors de la récupération des données :', error);
          }
    })
   }
}
