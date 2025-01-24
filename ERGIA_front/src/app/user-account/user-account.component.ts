import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { User, UpdateUserDTO } from '../../api/models/user';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

type EditableField = {
  key: keyof User;
  label: string;
  value: string;
  type: string;
  editMode: boolean;
};

@Component({
  selector: 'app-user-account',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-account.component.html',
  styleUrls: ['./user-account.component.scss'],
})
export class UserAccountComponent implements OnInit {
  user: User = {
    email: '',
    first_name: '',
    id_user: '',
    last_name: '',
  };

  editableFields: EditableField[] = [
    { key: 'first_name', label: 'Prénom', value: '', type: 'text', editMode: false },
    { key: 'last_name', label: 'Nom de famille', value: '', type: 'text', editMode: false },
    { key: 'email', label: 'Adresse email', value: '', type: 'email', editMode: false },
  ];

  passwordData = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  };

  errorMessage: string | null = null;
  successMessage: string | null = null;
  isEditing: boolean = false;

  constructor(
    private userService: UserService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const authToken = this.authService.getToken();
    if (authToken) {
      this.userService.getUser().subscribe({
        next: (data: User) => {
          this.user = data;
          this.updateEditableFields();
        },
        error: () => {
          this.errorMessage = 'Impossible de charger vos informations personnelles.';
        },
      });
    }
  }

  updateEditableFields(): void {
    this.editableFields.forEach((field) => {
      field.value = this.user[field.key] || '';
    });
  }

  toggleEditMode(field: EditableField, save = false): void {
    if (save) {
      // Prépare les données à envoyer à l'API
      const updateData: UpdateUserDTO = {};
      switch (field.key) {
        case 'first_name':
          updateData.firstname = field.value;
          break;
        case 'last_name':
          updateData.lastname = field.value;
          break;
        case 'email':
          updateData.email = field.value;
          break;
        default:
          this.errorMessage = `Le champ ${field.label} n'est pas modifiable.`;
          return;
      }
  
      // Appel au service pour mettre à jour l'utilisateur
      this.userService.updateUser(this.user.id_user, updateData).subscribe({
        next: () => {
          this.user[field.key] = field.value; // Mettez à jour la valeur localement
          this.successMessage = `${field.label} mis à jour avec succès.`;
          this.errorMessage = null;
        },
        error: (err) => {
          // Gestion des erreurs
          this.errorMessage = err.error?.message || `Erreur lors de la mise à jour de ${field.label}.`;
          this.successMessage = null;
        },
      });
    }
  
    // Bascule le mode édition
    field.editMode = !field.editMode;
    this.isEditing = this.editableFields.some((f) => f.editMode);
  }
  
  saveChanges(): void {
    this.errorMessage = null;
    this.successMessage = null;
  
    // Vérifie les mots de passe
    if (!this.passwordData.newPassword || !this.passwordData.confirmPassword) {
      this.errorMessage = 'Tous les champs de mot de passe doivent être remplis.';
      return;
    }
  
    if (this.passwordData.newPassword !== this.passwordData.confirmPassword) {
      this.errorMessage = 'Les mots de passe ne correspondent pas.';
      return;
    }
  
    const passwordPayload = {
      old_password: this.passwordData.currentPassword,
      new_password: this.passwordData.newPassword,
    };
  
    // Appel au service pour changer le mot de passe
    this.userService.changePassword(this.user.id_user, passwordPayload).subscribe({
      next: () => {
        this.successMessage = 'Mot de passe changé avec succès.';
        this.resetPasswordData();
        this.errorMessage = null;
      },
      error: (err) => {
        // Gestion des erreurs
        this.errorMessage = err.error?.message || 'Erreur lors du changement de mot de passe.';
        this.successMessage = null;
      },
    });
  }

  resetPasswordData(): void {
    this.passwordData.currentPassword = '';
    this.passwordData.newPassword = '';
    this.passwordData.confirmPassword = '';
  }

  confirmationDeleteAccount(): void {
    const confirmation = confirm('Êtes-vous sûr de vouloir supprimer votre compte ?');
    if (confirmation) {
      this.userService.deleteUser(this.user.id_user).subscribe({
        next: () => this.router.navigate(['/']),
        error: () => (this.errorMessage = 'Erreur lors de la suppression du compte.'),
      });
    }
  }
}
