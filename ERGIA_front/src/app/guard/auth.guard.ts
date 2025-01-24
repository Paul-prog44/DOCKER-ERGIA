import { CanActivateFn, RouterLink } from '@angular/router';
import { Router } from "@angular/router";
import { inject } from "@angular/core";
import { AuthService } from "../auth.service";

export const AuthGuard = (p0: unknown) => {
    const auth = inject(AuthService);
    const router = inject(Router);
    

    if(!auth.isLoggedIn()) {
        router.navigate(['/login'])
        return false
    }
    return true
}