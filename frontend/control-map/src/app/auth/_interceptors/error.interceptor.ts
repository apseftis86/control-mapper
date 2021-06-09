import { Injectable } from '@angular/core';
import {HttpRequest, HttpHandler, HttpEvent, HttpInterceptor} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import {AuthService} from '../_services/auth.service';
import {Router} from '@angular/router';
import {AlertService} from '../../alert/alert.service';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService,
              private alertService: AlertService,
              private router: Router) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(catchError(err => {
      let error = null;
      if (err.status === 401) {
        // auto logout if 401 response returned from api
        // this.alertService.alert('error', 'You have been logged out', false);
        this.authService.logout();
        location.reload(true);
      } else {
        if (err.error) {
          if (err.error.hasOwnProperty('non_field_errors')) {
            error = err.error.non_field_errors[0];
          } else {
            if (err.error instanceof Object) {
              err.error.detail ? error = err.error.detail :
                 (typeof err.error) === 'string' ? error = err.error : error = err.message;
            } else {
              error = err.error;
            }
          }
          if (!error || error.length > 200) {
            error = 'Unknown Error';
          }
          this.alertService.alert('error', error, true);
          return throwError(error);
        }
      }
    }));
  }
}
