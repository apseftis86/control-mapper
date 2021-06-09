import {Component, OnInit} from '@angular/core';
import {FileItem, FileUploader} from 'ng2-file-upload';
import {ActivatedRoute, Router} from '@angular/router';
import {environment} from '../../environments/environment';
import {AlertService} from '../alert/alert.service';

@Component({
  templateUrl: './import.component.html',
  styleUrls: ['./import.component.scss']
})
export class ImportComponent implements OnInit {
  fileUploader: FileUploader;
  itemsDropped = false;
  hasBaseDropZoneOver = false;
  hasAnotherDropZoneOver = false;
  queueLength = 0;
  userToken = JSON.parse(localStorage.getItem('authToken'));
  // application specific configs
  importCardTitle = 'Import New STIGS';
  alertMsgs = {
    success: 'Benchmark upload successful',
    error: 'Error uploading benchmark',
  };
  headers = [{name: 'Authorization', value: `JWT ${this.userToken}`}];
  url = `${environment.api}/stigs/upload_stig/`;
  constructor(public router: Router,
              public route: ActivatedRoute, private alertService: AlertService) {
    this.fileUploader = new FileUploader(
      {url: this.url, headers: this.headers});
  }
  ngOnInit() {
    this.fileUploader.onErrorItem = (item, response) => this.onErrorItem(item, response);
    this.fileUploader.onSuccessItem = (item, response) => this.onSuccessItem(item, response);
  }
  onErrorItem(item: FileItem, response: any): any {
    this.alertService.alert('error', this.alertMsgs.error);
  }
  onSuccessItem(item: FileItem, response: string): any {
    this.queueLength -= 1;
    this.alertService.alert('success', this.alertMsgs.success);
  }
  removeFromQueue(removeAll?: boolean) {
    if (removeAll) {
      this.queueLength = 0;
    } else {
      this.queueLength -= 1;
    }
  }
  // file import code
  public fileOverBase(e: any): void {
    this.hasBaseDropZoneOver = e;
  }
  public fileOverAnother(e: any): void {
    this.hasAnotherDropZoneOver = e;
  }
  public fileAccepted(): void {
    this.queueLength  = this.fileUploader.queue.filter(fileItem => !fileItem.isSuccess).length;
    if (this.itemsDropped) {
      return;
    } else {
      this.itemsDropped = !this.itemsDropped;
    }
  }
}
