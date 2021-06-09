import {Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild} from '@angular/core';
import {MatTableDataSource} from '@angular/material/table';
import {MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatDialog, MatDialogConfig} from '@angular/material/dialog';
import {ActivatedRoute, Router} from '@angular/router';
import {DialogComponent} from '../dialog/dialog.component';

@Component({
  selector: 'app-data-tables',
  templateUrl: './data-tables.component.html',
  styleUrls: ['./data-tables.component.scss'],
})
export class DataTablesComponent implements OnChanges {
  @ViewChild('sort', {static: true}) sort: MatSort;
  @ViewChild('paginator', {static: true}) paginator: MatPaginator;
  @Output() public emitAddItem = new EventEmitter();
  @Output() public emitDeleteItem = new EventEmitter();
  @Output() public emitUploadItem = new EventEmitter();
  @Output() public emitExportItem = new EventEmitter();
  @Output() public emitUpdateUser = new EventEmitter();
  @Output() public emitUpdateItem = new EventEmitter();
  @Output() public emitSelectItem = new EventEmitter();
  @Output() public emitDownloadItem = new EventEmitter();
  @Output() public emitProfileChange = new EventEmitter();
  @Input() public displayedColumns: any;
  @Input() public ssp: any;
  @Input() public endpoint: any;
  @Input() public placeholder: any;
  @Input() public defaultPagination: any;
  @Input() public availableActions: any = [];
  @Input() public items: any;
  @Input() public revision: number;
  @Input() public addPriv: boolean;
  @Input() public paginate = true;
  @Input() public pageSizeOptions = [10, 25, 50, 100, 200];
  @Input() public allowDownload: boolean;
  @Input() public loading: boolean;
  // for items that will reload the table on tab changes
  @Input() public reloading: boolean;
  @Input() public disableAddBtn: boolean;
  dt: MatTableDataSource<any>;
  noData: boolean;
  constructor(public matDialog: MatDialog, public router: Router, private route: ActivatedRoute) {}
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.items) {
      if (changes.items.currentValue) {
        this.dt = new MatTableDataSource<any>(this.items);
        if (this.paginate) {
          this.dt.paginator = this.paginator;
        }
        this.dt.sort = this.sort;
        try {
          this.noData = this.dt.filteredData.length === 0;
        } catch {
          this.noData = true;
        }
      }
    }
  }
  filterData(filterValue: string) {
    this.dt.filter = filterValue.trim().toLowerCase();
    this.checkData();
  }
  checkData() {
    try {
      this.noData = this.dt.filteredData.length === 0;
    } catch {
      this.noData = true;
    }
  }
  handleClick(row) {
    if (['stigs'].includes(this.endpoint)) {
      this.router.navigate([row.id], {relativeTo: this.route});
    } else if (['controls', 'ccis'].includes(this.endpoint)) {
      this.openRefDialog([row], this.endpoint);
    }
  }
  // dialog for the plugin modal screen
  openRefDialog(itemList, itemName) {
    const config = new MatDialogConfig();
    config.width = '875px';
    config['min-height'] = 'calc(100vh - 90px)';
    config.data = {
      item: itemList[0],
      type: itemName,
    };
    const dialogWindow = this.matDialog.open(DialogComponent, config);
    this.router.events.subscribe(() => {
      dialogWindow.close();
    });
    dialogWindow.afterClosed().subscribe((result) => {

    });
  }
  trackByFn(index, item) {
    return index;
  }
}
