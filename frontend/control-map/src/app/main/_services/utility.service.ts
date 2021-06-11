import {Injectable} from '@angular/core';
import {BehaviorSubject} from 'rxjs';
import {MatSnackBar} from '@angular/material/snack-bar';
import {MatDialogConfig} from '@angular/material/dialog';
import {Router} from '@angular/router';
import {ApiService} from './api.service';

@Injectable()
export class UtilityService {
  private breadcrumbsData = new BehaviorSubject<any[]>([]);
  private alertEvent = new BehaviorSubject<any>([]);
  private loading = new BehaviorSubject<boolean>(false);
  private updatedReportItem = new BehaviorSubject<any>(null);
  private windowSize = new BehaviorSubject<any>(window.innerWidth);
  private updatedReportItemCount = new BehaviorSubject<any>(null);
  exportTypes = {
    software: 'Software',
    users: 'Users',
    patch: 'Patches',
    fixes: 'Fix Texts',
  };
  constructor(
    public snackBar: MatSnackBar,
    private apiService: ApiService,
    private router: Router,
  ) {
  }
  setBreadcrumbs(message: any) {
    this.breadcrumbsData.next(message);
  }
  alert(messageObj: any, msgType: string) {
    this.alertEvent.next({type: msgType, message: messageObj});
  }
  get isLoading() {
    return this.loading.value;
  }
  setLoading(loading: boolean) {
    this.loading.next(loading);
  }
  get getBreadcrumbs() {
    return this.breadcrumbsData.value;
  }
  get updatedReportItemEvent() {
    return this.updatedReportItem.asObservable();
  }
  get getWindowSize() {
    return this.windowSize.asObservable();
  }
  get viewWindowSize() {
    return this.windowSize.value;
  }
  updateWindowSize(value: any) {
    this.windowSize.next(value);
  }
  updateReportItem(value: any) {
    this.updatedReportItem.next(value);
  }
  get updatedReportItemCountEvent() {
    return this.updatedReportItemCount.asObservable();
  }
  updateReportItemCount(value: any) {
    this.updatedReportItemCount.next(value);
  }
  capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
  makeSingular(str) {
    return str.substr(0, str.length - 1);
  }
  capitalizeSingularize(str) {
   return this.capitalize(this.makeSingular(str));
  }
  // openSnackbar(data: any, duration: any = 2000, verticalPosition: any = 'top') {
  //   const config = new MatSnackBarConfig();
  //   config.duration = duration !== 'indefinite' ? duration : null;
  //   config.verticalPosition = verticalPosition;
  //   config.data = data;
  //   return this.snackBar.openFromComponent(SnackbarComponent, config);
  // }
  // closeSnackbar() {
  //   this.snackBar.dismiss();
  // }
  configDialog(data: any, width: any, height = null) {
    const config = new MatDialogConfig();
    config['min-height'] = 'calc(100vh - 90px)';
    config.width = width;
    if (height) {
      config.height = height;
    }
    config.data = data;
    return config;
  }
  downloadToCSV(items, name): void {
    const header = ['ip address', 'system name', 'scanned at', 'outdated', 'compliance',
      'auth status', 'make', 'model', 'barcode', 'additional details', 'notes'];
    const csv = [];
    items.forEach(item => {
      const row = [];
      header.forEach(column => {
        if (column === 'auth status') {
          if (item.auth_status !== 'success') {
            row.push('FALSE');
          } else {
            row.push('TRUE');
          }
        } else {
          row.push(item[column.replace(' ', '_')]);
        }
      });
      csv.push(row);
    });
    csv.unshift(header.join(','));
    const csvArray = csv.join('\r\n');
    const anchor = document.createElement('a');
    const blob = new Blob([csvArray], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    anchor.href = url;
    anchor.download = `system-inventory-${name}.csv`;
    anchor.click();
    window.URL.revokeObjectURL(url);
    anchor.remove();
  }
  copyList(fromItem, type) {
    // this.openSnackbar({action: 'loading', type: this.capitalize(type)}, 'indefinite', 'bottom');
    let data = `${this.exportTypes[type]} List for SSP ${fromItem.name}: \n`;
    this.apiService.extraActionURL(`${this.router.url}/${type}_list`).subscribe((response: any) => {
      if (response.length === 0) {
        this.snackBar.open(`No ${this.exportTypes[type]} data to copy`, '', {duration: 3000, verticalPosition: 'bottom'});
      }
      response.forEach(item => {
        if (type !== 'fixes') {
          data += `\n Host: ${item.host} \n`;
          if (!['patch', 'fixes'].includes(type)) {
            data += `    ${this.exportTypes[type]}: \n`;
            item[type].forEach(i => {
              data += `        ${i}, \n`;
            });
          } else {
            const lines = item.patch_info.split('\n');
            lines.forEach(line => {
              if (line !== '') {
                data += `        ${line.replace(/\+/g, '')} \n`;
              }
            });
          }
        } else {
          data += `\n${item}\n`;
        }
      });
    });
    // this.closeSnackbar();
  }
}
