import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {CciComponent} from './cci/cci.component';
import {ControlComponent} from './control/control.component';
import {StigComponent} from './stig/stig.component';
import {MaterialModule} from '../material.module';
import {MultipleFieldFilterPipe} from './_filters/multiple-field-filter.pipe';
import {RulePipe} from './_filters/rule.pipe';
import {CciFilterPipe} from './_filters/cci-filter.pipe';
import {ApiService} from './_services/api.service';
import {FindingFilterPipe} from './_filters/finding.pipe';
import {FilterPipe} from './_filters/filter.pipe';
import {FormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {DataTablesComponent} from './data-tables/data-tables.component';
import {ComplianceReferenceComponent} from './compliance-reference/compliance-reference.component';
import {DialogComponent} from './dialog/dialog.component';
import {MainComponent} from './main.component';



@NgModule({
  declarations: [
    MainComponent,
    CciComponent,
    ControlComponent,
    StigComponent,
    MultipleFieldFilterPipe,
    RulePipe,
    CciFilterPipe,
    DialogComponent,
    DataTablesComponent,
    ComplianceReferenceComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    MaterialModule,
  ],
  providers: [
    ApiService,
    FindingFilterPipe,
    FilterPipe,
    CciFilterPipe,
    MultipleFieldFilterPipe
  ],
  exports: [],
  bootstrap: [MainComponent]
})
export class MainModule { }
