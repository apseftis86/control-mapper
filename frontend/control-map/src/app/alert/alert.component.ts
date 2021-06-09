import {Component, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from 'rxjs';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {AlertService} from './alert.service';
@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.scss'],
  animations: [
    trigger('alertExists', [
      state('show', style({opacity: '100%'})),
      state('hide', style({opacity: '0'})),
      transition('show => hide', animate('1500ms')),
    ]),
  ],
})
export class AlertComponent implements OnInit, OnDestroy {
  private subscription: Subscription;
  message: any;
  alertShow: boolean;
  alertSettings = {
    error: {timeout: 3000, color: 'bg-danger', icon: 'error'},
    info: {timeout: 2500, color: 'bg-info', icon: 'check_circle'},
    warning: {timeout: 2500, color: 'bg-info', icon: 'warning'},
    success: {timeout: 1500, color: 'bg-success', icon: 'check_circle'},
    logout: {timeout: 1500, color: 'bg-info', icon: 'warning'},
  };
  constructor(private alertService: AlertService) {

  }
  ngOnInit() {
    this.subscription = this.alertService.getAlert()
      .subscribe(message => {
        this.message = message;
        this.alertShow = true;
      });
  }
  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
  closeAlert() {
    setTimeout(() => {
      this.message = null;
    }, 1500);
  }
  onAnimate(event) {
    if (event.toState === 'show') {
      const timeout = this.alertSettings[this.message.type].timeout;
      setTimeout(() => {
        this.alertShow = false;
        this.closeAlert();
      }, timeout);
    }
  }
}
