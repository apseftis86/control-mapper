import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {take} from 'rxjs/operators';
import {ApiService} from '../_services/api.service';

@Component({
  selector: 'app-controls',
  templateUrl: './control.component.html',
  styleUrls: ['./control.component.scss']
})
export class ControlComponent implements OnInit {
  isList: boolean;
  loading: boolean = true;
  controls: any;
  constructor(private apiService: ApiService, private router: Router, private route: ActivatedRoute) {
    this.isList = this.route.snapshot.data.isList;
  }

  ngOnInit() {
    this.apiService.getFromURL(this.router.url + '/?revision=4').pipe(take(1)).subscribe((response) => {
      this.controls = response;
      this.loading = false;
    });
  }

}
