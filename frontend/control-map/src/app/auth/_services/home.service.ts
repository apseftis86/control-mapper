import {Injectable} from '@angular/core';
import {BehaviorSubject} from 'rxjs';

@Injectable()
export class HomeService {
  private consentSubject = new BehaviorSubject<any>(false);
  private windowSize = new BehaviorSubject<any>(window.innerWidth);
  constructor() {}
  get getWindowSize() {
    return this.windowSize.asObservable();
  }
  get viewWindowSize() {
    return this.windowSize.value;
  }
  updateWindowSize(value: any) {
    this.windowSize.next(value);
  }
  public get consentGrantedValue(): any {
    return this.consentSubject.value;
  }
  public get consent(): any {
    return this.consentSubject.asObservable();
  }
  public consentGranted(value): any {
    this.consentSubject.next(value);
  }
}
