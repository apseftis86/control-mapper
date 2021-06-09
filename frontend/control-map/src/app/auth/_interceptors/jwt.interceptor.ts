import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {

  constructor() {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // add authorization header with jwt token if available
    const userToken = JSON.parse(localStorage.getItem('authToken'));
    if (userToken) {
      request = request.clone({
        setHeaders: {
          Authorization: `JWT ${userToken}` }
      });
    }
    return next.handle(request);
  }
}
