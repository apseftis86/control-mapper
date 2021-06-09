import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {StigComponent} from './stig/stig.component';
import {ControlComponent} from './control/control.component';
import {CciComponent} from './cci/cci.component';
import {MainComponent} from './main.component';

const routes: Routes = [
  {path: 'dashboard', component: MainComponent},
  {path: 'stigs/:id', component: StigComponent, data: {isList: false}},
  {path: 'stigs', component: StigComponent, data: {isList: true}},
  {path: 'controls', component: ControlComponent, data: {isList: true}},
  {path: 'ccis', component: CciComponent, data: {isList: true}},
];
@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule { }
