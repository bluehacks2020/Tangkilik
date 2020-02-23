import { Injectable } from '@angular/core';
import { Storage } from '@ionic/storage';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MainControllerService {

  private API_URL = 'https://bluehacks.herokuapp.com/';

  constructor(private http: HttpClient, private storage: Storage) { }


  public async addToTemporaryCart(orderList: Array<object>): Promise<any> {
    return await this.storage.set('cart', orderList);
  }

  public async getCurrentCartContents(): Promise<any> {
    return await this.storage.get('cart');
  }

  public async initStorage(): Promise<any> {
    return await this.storage.ready();
  }

  public getProductList(): Observable<any> {
    return this.http.get(this.API_URL + '/READALL', { responseType: 'text' });
  }

  public async clearCartList(): Promise<any> {
    return this.storage.clear();
  }

}
