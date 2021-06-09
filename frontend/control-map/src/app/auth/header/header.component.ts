import {Component, Input, OnInit} from '@angular/core';
import {AuthService} from '../_services/auth.service';
import {MatDialog, MatDialogConfig} from '@angular/material/dialog';
import {Router} from '@angular/router';
import * as moment from 'moment';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  @Input() public appName: any;
  @Input() public content: any;
  links = [
    {route: '/stigs', text: 'STIGS'},
    {route: '/controls', text: 'Controls'},
    {route: '/ccis', text: 'CCIs'},
    {route: '/import', text: 'Import'},
  ];
  currentUser: any;
  constructor(public authService: AuthService,
              public router: Router,
              private matDialog: MatDialog) {
  }
  ngOnInit(): void {
    this.authService.currentUser.subscribe((user) => {
      if (user) {
      this.currentUser = user;
        if (this.currentUser.last_login !== 'None') {
          this.currentUser.last_login = moment(this.currentUser.last_login).format('M/D/YY LT');
        } else {
          this.currentUser.last_login = 'N/A';
        }
        if (this.currentUser.failed_login !== 'None') {
          this.currentUser.failed_login = moment(this.currentUser.failed_login).format('M/D/YY LT');
        } else {
          this.currentUser.failed_login = 'N/A';
        }
        this.authService.getExpireDate.subscribe((date) => {
          if (date) {
            const now = new Date();
            setTimeout(() => this.openDialog(), Number(date) - now.getTime() - 120000);
          }
        });
      } else {
        this.currentUser = null;
      }
    });
  }
  openDialog() {
    const config = new MatDialogConfig();
    config.width = '350px';
    config.data = {
      type: 'token',
    };
  }
}
