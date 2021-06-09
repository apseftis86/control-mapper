import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import {AuthService} from '../_services/auth.service';
import {HomeService} from '../_services/home.service';

@Injectable({ providedIn: 'root' })
export class LoginGuard implements CanActivate {
  constructor(
    private router: Router,
    private homeService: HomeService,
    private authService: AuthService,
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (this.authService.currentUserValue) {
      this.router.navigate(['/dashboard']);
      return false;
    }
    if (this.homeService.consentGrantedValue) {
      return true;
    }
    // not logged in so redirect to home page
    return true;
  }
}
