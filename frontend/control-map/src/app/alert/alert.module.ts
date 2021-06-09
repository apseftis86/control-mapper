import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {AlertComponent} from './alert.component';
import {AlertService} from './alert.service';
import {MatIconModule} from '@angular/material/icon';



@NgModule({
  declarations: [
    AlertComponent,
  ],
  imports: [
    CommonModule,
    MatIconModule,
  ],
  providers: [AlertService],
  exports: [AlertComponent]
})
export class AlertModule { }
