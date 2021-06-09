import {Component, OnInit} from '@angular/core';
import {AuthService} from '../_services/auth.service';
import {Router} from '@angular/router';
import {HomeService} from '../_services/home.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss', '../../../assets/animate.css'],
})
export class HomeComponent implements OnInit {
  constructor(public authService: AuthService,
              private router: Router,
              public homeService: HomeService) {}
  ngOnInit() {}
  acceptConsent() {
    this.homeService.consentGranted(true);
    this.router.navigate(['/']);
  }
}
