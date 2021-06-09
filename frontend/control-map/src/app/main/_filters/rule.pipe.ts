import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'rule',
  pure: false,
})
export class RulePipe implements PipeTransform {

  transform(rules: any, selectedProfile: any): unknown {
    if (!rules) {
      return;
    }
    if (!selectedProfile) {
      return rules;
    }
    return rules.filter(r => {
      return selectedProfile.selects.includes(r.vuln_id) || selectedProfile.selects.includes(r.rule_id)
    });
  }

}
