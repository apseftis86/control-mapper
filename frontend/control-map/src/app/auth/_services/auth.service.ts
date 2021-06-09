// System imports
import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, Observable} from 'rxjs';
import {Router} from '@angular/router';
import {map} from 'rxjs/operators';

// Local imports
import * as jwt from 'jwt-decode';
import {MatDialog} from '@angular/material/dialog';
import {environment} from '../../../environments/environment';
import {HomeService} from './home.service';
import {AlertService} from '../../alert/alert.service';

@Injectable({providedIn: 'root'})

export class AuthService {
    private loginServer = `${environment.api}/get-token/`;
    private registerServer = `${environment.api}/register/`;
    private refreshTokenServer = `${environment.api}/refresh-token/`;
    private currentUserSubject: BehaviorSubject<any>;
    public currentUser: Observable<any>;
    private expireDate = new BehaviorSubject<any>(null);
    constructor(private http: HttpClient, private router: Router,
                private alertService: AlertService,
                public matDialog: MatDialog, private homeService: HomeService) {
      let token = JSON.parse(localStorage.getItem('authToken'));
      if (token) {
        token = jwt(token);
        this.expireDate.next(token.exp * 1000);
        this.homeService.consentGranted(true);
      }
      this.currentUserSubject = new BehaviorSubject<any>(token);
      this.currentUser = this.currentUserSubject.asObservable();
    }
    public get currentUserValue(): any {
        return this.currentUserSubject.value;
    }
    get getExpireDate(): any {
      return this.expireDate.asObservable();
    }
    login(name: string, pass: string): any {
        return this.http.post<any>(this.loginServer,
            {username: name, password: pass})
            .pipe(map(user => {
                // login successful if there's a jwt token in the response
                if (user && user.token) {
                    localStorage.setItem('authToken', JSON.stringify(user.token));
                    this.currentUserSubject.next(jwt(user.token));
                    this.expireDate.next(jwt(user.token).exp * 1000);
                }
            }));
    }
    register(user: any) {
      return this.http.post<any>(this.registerServer, user, {
        headers: {'Content-Type' : 'application/json'},  withCredentials: true
      }).pipe(map( message => {
        return message;
      }, error => {
        return error;
      }));
    }
  refreshToken() {
    const authToken = JSON.parse(localStorage.getItem('authToken'));
    return this.http.post<any>(this.refreshTokenServer, {token: authToken}).pipe(map((user: any) => {
      if (user) {
        localStorage.setItem('authToken', JSON.stringify(user.token));
        this.currentUserSubject.next(jwt(user.token));
        this.expireDate.next(jwt(user.token).exp * 1000);
      }
    }));
  }
    logout() {
      this.router.navigate(['/']);
      this.alertService.alert('logout', 'You have been logged out', false);
      // remove user from local storage to log user out
      localStorage.removeItem('authToken');
      this.currentUserSubject.next(null);
      this.expireDate.next(null);
      this.homeService.consentGranted(false);
      this.matDialog.closeAll();
    }
}


