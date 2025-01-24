import { TestBed } from '@angular/core/testing';
import { UserAccountComponent } from './user-account.component';
import { UserService } from '../services/user.service';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';

type EditableField = {
    key: keyof User;
    label: string;
    value: string;
    type: string;
    editMode: boolean;
  };

  type User = {
    email: string;
    first_name: string;
    id_user: string;
    last_name: string;
  };

describe('UserAccountComponent', () => {
  let component: UserAccountComponent;
  let userServiceSpy: jasmine.SpyObj<UserService>;
  let authServiceSpy: jasmine.SpyObj<AuthService>;
  let routerSpy: jasmine.SpyObj<Router>;

  beforeEach(() => {
    userServiceSpy = jasmine.createSpyObj('UserService', ['getUser', 'updateUser', 'changePassword', 'deleteUser']);
    authServiceSpy = jasmine.createSpyObj('AuthService', ['getToken']);
    routerSpy = jasmine.createSpyObj('Router', ['navigate']);

    TestBed.configureTestingModule({
      imports: [UserAccountComponent],
      providers: [
        { provide: UserService, useValue: userServiceSpy },
        { provide: AuthService, useValue: authServiceSpy },
        { provide: Router, useValue: routerSpy },
      ],
    });

    const fixture = TestBed.createComponent(UserAccountComponent);
    component = fixture.componentInstance;
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should fetch user data if token is available', () => {
      const mockUser = {
        email: 'test@example.com',
        first_name: 'John',
        id_user: '123',
        last_name: 'Doe',
      };
      authServiceSpy.getToken.and.returnValue('mock-token');
      userServiceSpy.getUser.and.returnValue(of(mockUser));

      component.ngOnInit();

      expect(component.user).toEqual(mockUser);
      expect(component.editableFields[0].value).toEqual('John');
    });

    it('should set an error message if user data fetch fails', () => {
      authServiceSpy.getToken.and.returnValue('mock-token');
      userServiceSpy.getUser.and.returnValue(throwError(() => new Error('Fetch failed')));

      component.ngOnInit();

      expect(component.errorMessage).toEqual('Impossible de charger vos informations personnelles.');
    });
  });

  describe('toggleEditMode', () => {
    it('should save updated field data and toggle edit mode off', () => {
      const mockField: EditableField = {
        key: 'first_name', // clé valide de type keyof User
        label: 'Prénom',
        value: 'John',
        type: 'text',
        editMode: true,
      };
      const mockUpdateData = { firstname: 'John' };

      component.user.id_user = '123';
      userServiceSpy.updateUser.and.returnValue(of(null));
      component.toggleEditMode(mockField, true);

      expect(userServiceSpy.updateUser).toHaveBeenCalledWith('123', mockUpdateData);
      expect(mockField.editMode).toBeFalse();
      expect(component.successMessage).toEqual('Prénom mis à jour avec succès.');
    });

    it('should set an error message if update fails', () => {
      const mockField: EditableField = {
        key: 'first_name',
        label: 'Prénom',
        value: 'John',
        type: 'text',
        editMode: true,
      };

      component.user.id_user = '123';
      userServiceSpy.updateUser.and.returnValue(throwError(() => new Error('Update failed')));
      component.toggleEditMode(mockField, true);

      expect(component.errorMessage).toEqual('Erreur lors de la mise à jour de Prénom.');
    });
  });

  describe('saveChanges', () => {
    it('should change the password successfully', () => {
      component.user.id_user = '123';
      component.passwordData = {
        currentPassword: 'oldPass123!',
        newPassword: 'newPass123!',
        confirmPassword: 'newPass123!',
      };
      userServiceSpy.changePassword.and.returnValue(of(null));

      component.saveChanges();

      expect(userServiceSpy.changePassword).toHaveBeenCalledWith('123', {
        old_password: 'oldPass123!',
        new_password: 'newPass123!',
      });
      expect(component.successMessage).toEqual('Mot de passe changé avec succès.');
    });

    it('should set an error if passwords do not match', () => {
      component.passwordData = {
        currentPassword: 'oldPass123!',
        newPassword: 'newPass123!',
        confirmPassword: 'wrongPass',
      };

      component.saveChanges();

      expect(component.errorMessage).toEqual('Les mots de passe ne correspondent pas.');
    });

    it('should set an error if password change fails', () => {
      component.user.id_user = '123';
      component.passwordData = {
        currentPassword: 'oldPass123!',
        newPassword: 'newPass123!',
        confirmPassword: 'newPass123!',
      };
      userServiceSpy.changePassword.and.returnValue(throwError(() => new Error('Change failed')));

      component.saveChanges();

      expect(component.errorMessage).toEqual('Erreur lors du changement de mot de passe.');
    });
  });

  describe('confirmationDeleteAccount', () => {
    it('should delete the user account and navigate to home', () => {
      spyOn(window, 'confirm').and.returnValue(true);
      component.user.id_user = '123';
      userServiceSpy.deleteUser.and.returnValue(of(null));

      component.confirmationDeleteAccount();

      expect(userServiceSpy.deleteUser).toHaveBeenCalledWith('123');
      expect(routerSpy.navigate).toHaveBeenCalledWith(['/']);
    });

    it('should set an error message if account deletion fails', () => {
      spyOn(window, 'confirm').and.returnValue(true);
      component.user.id_user = '123';
      userServiceSpy.deleteUser.and.returnValue(throwError(() => new Error('Deletion failed')));

      component.confirmationDeleteAccount();

      expect(component.errorMessage).toEqual('Erreur lors de la suppression du compte.');
    });
  });
});
