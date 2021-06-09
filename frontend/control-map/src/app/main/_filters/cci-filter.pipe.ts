import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'cciFilter',
  pure: false
})
export class CciFilterPipe implements PipeTransform {
  transform(items: any[], searchText: string, nistFilter: string, benchmarkFilters: any): any[] {
    if (!searchText) {
      if (nistFilter) {
        items = items.filter(i => i.nist_family === nistFilter);
      }
      return items.filter(item =>
          item.checks.filter(i => benchmarkFilters.includes(i.name)).length > 0);
      }
    if (!items) {
      return [];
    } else {
      return items.filter(it => {
        if (nistFilter) {
          return it.name.toLowerCase().includes(searchText.toLowerCase()) && it.nist_family === nistFilter && it.checks.filter(i => benchmarkFilters.includes(i.name)).length > 0;
        }
        return it.name.toLowerCase().includes(searchText.toLowerCase()) && it.checks.filter(i => benchmarkFilters.includes(i.name)).length > 0;
      });
    }
  }
}
