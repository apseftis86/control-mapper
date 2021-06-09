import {Component, Input, OnInit, EventEmitter, Output, AfterViewInit} from '@angular/core';
import {FileItem, FileUploader} from 'ng2-file-upload';
import {environment} from '../../../environments/environment';
import {ActivatedRoute, Router} from '@angular/router';
import {ApiService} from '../_services/api.service';
import {take} from 'rxjs/operators';

@Component({
  selector: 'app-stig',
  templateUrl: './stig.component.html',
  styleUrls: ['./stig.component.scss']
})
export class StigComponent implements OnInit {
  isList: boolean;
  loading: boolean;
  showChecksFixes = true;
  stigs: any;
  stig: any;
  rules: any;
  nistRevision = 4;
  selectedProfile: any;
  searchText: any;
  readableSeverity = {
    info: {class: 'badge badge-info'},
    low: {class: 'badge badge-success'},
    medium: {class: 'badge badge-warning'},
    high: {class: 'badge bg-high text-white'},
    unknown: {class: 'badge badge-secondary'},
  } as any;
  ruleFilters = new Set(['title', 'description', 'rule_id', 'vuln_id', 'severity', 'searchable_cci']);
  constructor(public apiService: ApiService,  public router: Router,
              public route: ActivatedRoute) {
    this.isList = this.route.snapshot.data.isList;
    this.loading = true;
  }
  toggleRuleFilters(value: string): void {
    this.ruleFilters.has(value) ? this.ruleFilters.delete(value) : this.ruleFilters.add(value);
  }
  updateRules(): void {
    this.rules = this.stig.rules.filter(r =>
      this.selectedProfile.selects.includes(r.vuln_id) || this.selectedProfile.selects.includes(r.rule_id)
    )
  }
  toggleChecksFixes(): void{
    this.showChecksFixes = ! this.showChecksFixes
  }
  ngOnInit() {
    this.apiService.getFromURL(this.router.url + '/').pipe(take(1)).subscribe((response) => {
      if (this.isList) {
        this.stigs = response;
      } else {
        this.stig = response;
        this.stig.rules.forEach(rule => {
          rule.searchable_cci = rule.ccis.join(',');
        });
        this.rules = this.stig.rules;
      }
      this.loading = false;
    });
  }
}
