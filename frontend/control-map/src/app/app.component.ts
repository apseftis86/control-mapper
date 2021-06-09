import {Component, OnInit} from '@angular/core';
import {MatIconRegistry} from '@angular/material/icon';
import {DomSanitizer} from '@angular/platform-browser';
import {AuthService} from './auth/_services/auth.service';
import {Router} from '@angular/router';
import {HomeService} from './auth/_services/home.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'NIST Map';
  consentApproved$: any;
  constructor(public router: Router, private matIconRegistry: MatIconRegistry,
              private domSanitizer: DomSanitizer, public homeService: HomeService,
              public authService: AuthService) {
    this.matIconRegistry.addSvgIcon(
      'file_pie',
      // this is a Font Awesome Icon, I do have license to use
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/font-awesome-svg/file-chart-pie-regular.svg')
    ).addSvgIcon(
      'check_off',
      // this is a Font Awesome Icon, I do have license to use
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/font-awesome-svg/ballot-check-regular.svg')
    ).addSvgIcon(
      'upload',
      // this is a Font Awesome Icon, I do have license to use
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/font-awesome-svg/upload-regular.svg')
    ).addSvgIcon(
      'chart_network',
      // this is a Font Awesome Icon, I do have license to use
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/font-awesome-svg/chart-network-regular.svg')
    ).addSvgIcon(
      'analytics',
      // this is a Font Awesome Icon, I do have license to use
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/font-awesome-svg/analytics-regular.svg')
    ).addSvgIcon(
      'share',
      // this is a Font Awesome Icon, I do have license to use
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/font-awesome-svg/share-all-regular.svg')
    ).addSvgIcon(
      'paste',
      // this is a Font Awesome Icon, I do have license to use
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/font-awesome-svg/paste-solid.svg')
    ).addSvgIcon(
      'download',
      // this is a Font Awesome Icon, I do have license to use
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/font-awesome-svg/file-download-regular.svg')
    ).addSvgIcon(
      'cat-solid',
      // this is a Font Awesome Icon, I do have license to use
      this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/font-awesome-svg/cat-solid.svg')
    );
  }
  ngOnInit(): void {
    this.homeService.consent.subscribe((consent) => {
      this.consentApproved$ = consent;
    });
  }
}
