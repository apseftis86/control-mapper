import {Component, Input, OnInit} from '@angular/core';
import {MatDialog, MatDialogConfig} from '@angular/material/dialog';
import {MatSnackBar, MatSnackBarConfig} from '@angular/material/snack-bar';
import {ActivatedRoute, Router} from '@angular/router';
import {DialogComponent} from '../dialog/dialog.component';
import {ApiService} from '../_services/api.service';

@Component({
  selector: 'app-compliance-reference',
  templateUrl: './compliance-reference.component.html',
  styleUrls: ['./compliance-reference.component.scss']
})
export class ComplianceReferenceComponent implements OnInit {
  @Input() public reference: {name: string, text: string, revision?: number};
  returnedValues = [];
  constructor(public apiService: ApiService, public route: ActivatedRoute, private matDialog: MatDialog,
              private snackBar: MatSnackBar,
              public router: Router) {}

  ngOnInit() {
  }
  selectRef() {
    let lookup;
    const endpoint = 'rules';
    if (['group-id', 'vuln-id'].includes(this.reference.name.toLowerCase().replace('_', '-'))) {
      lookup = 'vuln_id';
    } else if (this.reference.name.toLowerCase().replace('_', '-') === 'rule-id') {
      lookup = 'rule_id';
    } else if (this.reference.name.toLowerCase().replace('_', '-') === 'stig-id') {
      lookup = 'version';
    } else if (!['800-53', 'CCI', '800-171'].includes(this.reference.name)) {
      const config = new MatSnackBarConfig();
      config.duration = 1500;
      config.verticalPosition = 'top';
      this.snackBar.open('Reference could not be mapped to a database object', '', config);
      return;
    }
    const seenBefore = this.returnedValues.find(v => v.lookUp === this.reference.text);
    if (!seenBefore) {
      if (!['800-53', 'CCI'].includes(this.reference.name)) {
        this.apiService.getFilteredItems(`${endpoint}/item-map/?${lookup}=${this.reference.text}`).subscribe((objs) => {
          if (objs.length > 0) {
            this.openRefDialog(objs, this.reference.text);
          } else {
            this.noItemsMatch();
          }
        });
      } else {
        if (this.reference.name === '800-53') {
          this.apiService.getFilteredItems(`controls/?revision=${this.reference.revision}&statements__number=${this.reference.text}`).subscribe((items) => {
            if (items.length === 0) {
              this.noItemsMatch();
            } else {
              this.returnedValues.push({lookUp: `${this.reference.text}r${this.reference.revision}`,  itemName: 'NIST',  result: items});
              this.openRefDialog(items, 'controls');
            }
          });
        } else if (this.reference.name === 'CCI') {
          this.apiService.getFilteredItems(`ccis/?name=${this.reference.text}`).subscribe((item) => {
            if (item) {
              this.returnedValues.push({lookUp: this.reference.text,  itemName: 'CCI',  result: item});
              this.openRefDialog(item, 'ccis');
            } else {
              this.noItemsMatch();
            }
          });
        }
      }
    } else {
      this.openRefDialog(seenBefore.result, seenBefore.itemName);
    }
  }
  noItemsMatch() {
    // wont be checking for any other cases.
    const config = new MatSnackBarConfig();
    config.duration = 1500;
    config.verticalPosition = 'top';
    this.snackBar.open('No items match search', '', config);
  }
  // dialog for the plugin modal screen
  openRefDialog(itemList, itemName) {
    const config = new MatDialogConfig();
    config.width = '875px';
    config['min-height'] = 'calc(100vh - 90px)';
    if (!['controls', 'ccis', 'NIST-800-171'].includes(itemName)) {
      config.data = {
        items: itemList,
        type: 'rules',
        name: itemName
      };
    } else {
      config.data = {
        item: itemList[0],
        type: itemName,
      };
    }
    const dialogWindow = this.matDialog.open(DialogComponent, config);
    this.router.events.subscribe(() => {
      dialogWindow.close();
    });
    dialogWindow.afterClosed().subscribe((result) => {

    });
  }
}
