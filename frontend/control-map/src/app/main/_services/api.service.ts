import { Injectable } from '@angular/core';
import {environment} from '../../../environments/environment';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  protected headers = new HttpHeaders({'Content-Type': 'application/json'});

  constructor(protected http: HttpClient) { }
  // basic functions for items
  // for nested URL patterns that will not have specific id
  getFromURL(url: string): Observable<any> {
    return this.http.get(`${environment.api}${url}`, {headers: this.headers});
  }
  // for nested URL patterns that will not have specific id
  extraActionURL(url: string): Observable<any> {
    return this.http.get(`${environment.api}${url}/`, {headers: this.headers});
  }
  // specialized functions for items such as filtering (some urls will include filters inside of functions in components)
  getFilteredItems(endpoint: string): Observable<any> {
    const url = `${environment.api}/${endpoint}`;
    return this.http.get(url, {headers: this.headers});
  }
}
