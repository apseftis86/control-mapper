import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {SnackbarComponent} from './snackbar.component';
import {MatIconModule} from '@angular/material/icon';



@NgModule({
  declarations: [
    SnackbarComponent
  ],
  imports: [
    CommonModule,
    MatProgressSpinnerModule,
    MatIconModule,
  ]
})
export class SnackbarModule { }
