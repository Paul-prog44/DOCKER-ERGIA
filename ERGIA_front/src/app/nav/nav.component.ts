import { Component } from '@angular/core';
import {Router, RouterLink, RouterOutlet,RouterModule} from "@angular/router";
import { AuthService } from '../auth.service';
import {NgIf} from "@angular/common";




@Component({
  selector: 'app-nav',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    RouterModule,
    NgIf
  ],
  templateUrl: './nav.component.html',
  styleUrl: './nav.component.scss'
})
export class NavComponent {
  constructor(private authService: AuthService, private router: Router) {}

  isConnect() {
    return this.authService.isLoggedIn();
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/']);
  }

  reloadPage(event: Event): void {
    this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
      this.router.navigate(['/campaignDashboard']);
    });
  }
}
