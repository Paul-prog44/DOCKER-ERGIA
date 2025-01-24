import { Component, EventEmitter, input, output, Output } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { AnnotationService } from '../../services/annotation.service';
import { Annotation } from '../../../api/models/annotation';

@Component({
  selector: 'app-modal-annotation',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './modal-annotation.component.html',
  styleUrl: './modal-annotation.component.scss'
})
export class ModalAnnotationComponent {

  constructor(private annotationService: AnnotationService) {}

  @Output() close = new EventEmitter<void>();
  addAnnotation = output<Annotation>()
  errorMessage = ""

  index = input(0)
  length = input(0)
  annotations = input<Annotation[]>()

  addAnnotationForm = new FormGroup({
    oldScu : new FormControl(''),
    scu : new FormControl(''),
    color: new FormControl(''),
  })

  closePopup() {
	this.close.emit();
  }

  handleAddAnnotation() {
    if (this.addAnnotationForm.value.oldScu != "") {
      for (let oldAnnotation of this.annotations()!) {
        if (oldAnnotation.scu == this.addAnnotationForm.value.oldScu) {
          const annotation : Annotation = {
            scu : oldAnnotation.scu,
            color : oldAnnotation.color,
            summary_id : oldAnnotation.summary_id,
            index : this.index(),
            length : this.length(),
            creator : oldAnnotation.creator
          }
      
          this.addAnnotation.emit(annotation)
          this.closePopup()
          return
        } else {
          console.log("Aucune annotation correspondante trouvée");
        }
      }
      return
    }
    
    if (!this.addAnnotationForm.value.scu) {
      this.errorMessage="Vous devez mettre une Scu"
      return
    }


    const annotation : Annotation = {
      scu : this.addAnnotationForm.value.scu!,
      color : this.addAnnotationForm.value.color!,
      summary_id : 12, //A récuperer
      index : this.index(),
      length : this.length(),
      creator : 42 // A récuperer
    }

    this.addAnnotation.emit(annotation)
    // this.annotationService.createAnnotation(annotation)
    this.closePopup()
  }
}
