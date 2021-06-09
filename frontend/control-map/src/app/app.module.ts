import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {CommonModule} from '@angular/common';
import {AuthModule} from './auth/auth.module';
import {AuthRoutingModule} from './auth/auth-routing.module';
import {AlertModule} from './alert/alert.module';
import {MainModule} from './main/main.module';
import {MainRoutingModule} from './main/main-routing.module';
import {ImportModule} from './import/import.module';
import {ImportRoutingModule} from './import/import-routing.module';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    CommonModule,
    AppRoutingModule,
    AuthModule,
    AuthRoutingModule,
    AlertModule,
    MainModule,
    MainRoutingModule,
    ImportModule,
    ImportRoutingModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule { }
