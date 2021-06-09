import { Component, OnInit } from '@angular/core';
import {take} from 'rxjs/operators';
import {ApiService} from '../_services/api.service';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-cci',
  templateUrl: './cci.component.html',
  styleUrls: ['./cci.component.scss']
})
export class CciComponent implements OnInit {
  isList: boolean;
  loading: boolean = true;
  ccis: any;
  nistRevision = 4;
  constructor(private apiService: ApiService, private router: Router, private route: ActivatedRoute) {
    this.isList = this.route.snapshot.data.isList;
  }
  ngOnInit() {
    this.apiService.getFromURL(this.router.url + '/').pipe(take(1)).subscribe((response) => {
      this.ccis = response;
      this.loading = false;
    });
  }

}
