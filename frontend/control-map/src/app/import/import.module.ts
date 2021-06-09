import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ImportComponent} from './import.component';
import {MaterialModule} from '../material.module';
import {FileUploadModule} from 'ng2-file-upload';



@NgModule({
  declarations: [
    ImportComponent,
  ],
  imports: [
    CommonModule,
    FileUploadModule,
    MaterialModule,
  ],
})
export class ImportModule { }
